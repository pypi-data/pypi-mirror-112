#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""RAMSES RF - The evohome-compatible system."""

import logging
from asyncio import Task
from datetime import timedelta as td
from inspect import getmembers, isclass
from sys import modules
from threading import Lock
from types import SimpleNamespace
from typing import List, Optional

from .command import Command, FaultLog, Priority
from .const import (
    _000C_DEVICE,
    _0005_ZONE,
    ATTR_DEVICES,
    DEVICE_HAS_ZONE_SENSOR,
    DISCOVER_ALL,
    DISCOVER_PARAMS,
    DISCOVER_SCHEMA,
    DISCOVER_STATUS,
    SystemMode,
    SystemType,
    __dev_mode__,
)
from .devices import BdrSwitch, Device, Entity, OtbGateway
from .exceptions import CorruptStateError, ExpiredCallbackError
from .schema import (
    ATTR_CONTROLLER,
    ATTR_DHW_SYSTEM,
    ATTR_HTG_CONTROL,
    ATTR_HTG_SYSTEM,
    ATTR_ORPHANS,
    ATTR_UFH_SYSTEM,
    ATTR_ZONES,
)
from .zones import DhwZone, Zone, create_zone

I_, RQ, RP, W_ = " I", "RQ", "RP", " W"

DEV_MODE = __dev_mode__ and False

_LOGGER = logging.getLogger(__name__)
if DEV_MODE:
    _LOGGER.setLevel(logging.DEBUG)


SYSTEM_CLASS = SimpleNamespace(
    EVO="evohome",  # Stored HW (not a zone)
    PRG="programmer",  # Electric
)


class SysFaultLog:  # 0418
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._fault_log = FaultLog(self._ctl)

    def _discover(self, discover_flag=DISCOVER_ALL) -> None:
        super()._discover(discover_flag=discover_flag)

        if discover_flag & DISCOVER_STATUS:
            self._gwy._tasks.append(self._loop.create_task(self.get_fault_log()))

    async def get_fault_log(self, force_refresh=None) -> Optional[dict]:  # 0418
        try:
            return await self._fault_log.get_fault_log(force_refresh=force_refresh)
        except ExpiredCallbackError:
            return

    @property
    def status(self) -> dict:
        status = super().status
        # assert "fault_log" not in status  # TODO: removeme
        status["fault_log"] = self._fault_log.fault_log
        status["last_fault"] = self._msgz[I_].get("0418")
        return status


class SysDatetime:  # 313F
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._datetime = None

    def _discover(self, discover_flag=DISCOVER_ALL) -> None:
        super()._discover(discover_flag=discover_flag)

        if discover_flag & DISCOVER_STATUS:
            self._gwy.send_cmd(Command.get_system_time(self.id), period=td(hours=1))

    def _handle_msg(self, msg, prev_msg=None):
        super()._handle_msg(msg)

        if msg.code == "313F" and msg.verb in (I_, RP):  # TODO: W
            self._datetime = msg

    @property
    def datetime(self) -> Optional[str]:
        return self._msg_payload(self._datetime, "datetime")  # TODO: make a dt object

    # def wait_for(self, cmd, callback):
    # self._api_lock.acquire()

    # self._send_cmd("313F", verb=RQ, callback=callback)

    #     time_start = dt.now()
    # while not self._schedule_done:
    #     await asyncio.sleep(TIMER_SHORT_SLEEP)
    #     if dt.now() > time_start + TIMER_LONG_TIMEOUT:
    #         self._api_lock.release()
    #         raise ExpiredCallbackError("failed to set schedule")

    # self._api_lock.release()

    # async def get_datetime(self) -> str:  # wait for the RP/313F
    # await self.wait_for(Command("313F", verb=RQ))
    # return self.datetime

    # async def set_datetime(self, dtm: dt) -> str:  # wait for the I/313F
    # await self.wait_for(Command("313F", verb=W_, payload=f"00{dtm_to_hex(dtm)}"))
    # return self.datetime

    @property
    def status(self) -> dict:
        status = super().status
        # assert ATTR_HTG_SYSTEM in status  # TODO: removeme
        # assert "datetime" not in status[ATTR_HTG_SYSTEM]  # TODO: removeme
        status[ATTR_HTG_SYSTEM]["datetime"] = self.datetime
        return status


class SysLanguage:  # 0100
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._language = None

    def _discover(self, discover_flag=DISCOVER_ALL) -> None:
        super()._discover(discover_flag=discover_flag)

        if discover_flag & DISCOVER_PARAMS:
            # self._send_cmd("0100")  # language
            self._gwy.send_cmd(Command.get_system_language(self.id))

    def _handle_msg(self, msg, prev_msg=None):
        super()._handle_msg(msg)

        if msg.code == "0100" and msg.verb in (I_, RP):
            self._language = msg

    @property
    def language(self) -> Optional[str]:  # 0100
        return self._msg_payload(self._language, "language")

    @property
    def params(self) -> dict:
        params = super().params
        # assert ATTR_HTG_SYSTEM in params  # TODO: removeme
        # assert "language" not in params[ATTR_HTG_SYSTEM]  # TODO: removeme
        params[ATTR_HTG_SYSTEM]["language"] = self.language
        return params


class SysMode:  # 2E04
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._system_mode = None

    def _discover(self, discover_flag=DISCOVER_ALL) -> None:
        super()._discover(discover_flag=discover_flag)

        if discover_flag & DISCOVER_STATUS:
            self._gwy.send_cmd(Command.get_system_mode(self.id), period=td(hours=1))

    def _handle_msg(self, msg, prev_msg=None):
        super()._handle_msg(msg)

        if msg.code == "2E04" and msg.verb in (I_, RP):  # this is a special case
            self._system_mode = msg

    @property
    def system_mode(self) -> Optional[dict]:  # 2E04
        return self._msg_payload(self._system_mode)

    def set_mode(self, system_mode=None, until=None) -> Task:
        """Set a system mode for a specified duration, or indefinitely."""
        cmd = Command.set_system_mode(self.id, system_mode=system_mode, until=until)
        return self._gwy.send_cmd(cmd)

    def set_auto(self) -> Task:
        """Revert system to Auto, set non-PermanentOverride zones to FollowSchedule."""
        return self.set_mode(SystemMode.AUTO)

    def reset_mode(self) -> Task:
        """Revert system to Auto, force *all* zones to FollowSchedule."""
        return self.set_mode(SystemMode.RESET)

    @property
    def params(self) -> dict:
        params = super().params
        # assert ATTR_HTG_SYSTEM in params  # TODO: removeme
        # assert "system_mode" not in params[ATTR_HTG_SYSTEM]  # TODO: removeme
        params[ATTR_HTG_SYSTEM]["system_mode"] = self.system_mode
        return params


class StoredHw:
    MIN_SETPOINT = 30.0  # NOTE: these may be removed
    MAX_SETPOINT = 85.0
    DEFAULT_SETPOINT = 50.0

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._dhw = None

    def _handle_msg(self, msg, prev_msg=None):
        def find_dhw_sensor(this) -> None:
            """Eavesdrop packets, or pairs of packets, to maintain the system state.

            There are only 2 ways to to find a controller's DHW sensor:
            1. The 10A0 RQ/RP *from/to a 07:* (1x/4h) - reliable
            2. Use sensor temp matching - non-deterministic

            Data from the CTL is considered more authorative. The RQ is initiated by the
            DHW, so is not authorative. The I/1260 is not to/from a controller, so is
            not useful.
            """

            # 10A0: RQ/07/01, RP/01/07: can get both parent controller & DHW sensor
            # 047 RQ --- 07:030741 01:102458 --:------ 10A0 006 00181F0003E4
            # 062 RP --- 01:102458 07:030741 --:------ 10A0 006 0018380003E8

            # 1260: I/07: can't get which parent controller - would need to match temps
            # 045  I --- 07:045960 --:------ 07:045960 1260 003 000911

            # 1F41: I/01: get parent controller, but not DHW sensor
            # 045  I --- 01:145038 --:------ 01:145038 1F41 012 000004FFFFFF1E060E0507E4
            # 045  I --- 01:145038 --:------ 01:145038 1F41 006 000002FFFFFF

            if all(
                (
                    this.code == "10A0",
                    this.verb == RP,
                    this.src is self._ctl,
                    this.dst.type == "07",
                )
            ):
                self._dhw = self._get_dhw(sensor=this.dst)

        super()._handle_msg(msg)

        if msg.code == "10A0":  # dhw_params
            if msg._gwy.config.enable_eavesdrop:
                find_dhw_sensor(msg)

        elif msg.code == "1260":  # dhw_temp
            pass

        elif msg.code == "1F41":  # dhw_mode
            pass

    def _get_dhw(self, **kwargs) -> DhwZone:
        """Return the DHW zone (will create/update it if required)."""

        # NOTE: kwargs not passed, so discovery is as eavesdropping
        dhw = self.dhw or create_zone(self, zone_idx="HW")

        if kwargs.get("sensor"):
            dhw._set_sensor(kwargs["sensor"])

        if kwargs.get("dhw_valve"):
            dhw._set_dhw_valve(kwargs["dhw_valve"])

        if kwargs.get("htg_valve"):
            dhw._set_htg_valve(kwargs["htg_valve"])

        return dhw

    @property
    def dhw(self) -> DhwZone:
        return self._dhw

    def _set_dhw(self, dhw: DhwZone) -> None:  # self._dhw
        """Set the DHW zone system."""

        if not isinstance(dhw, DhwZone):
            raise TypeError(f"stored_hw can't be: {dhw}")

        if self._dhw is not None:
            if self._dhw is dhw:
                return
            raise CorruptStateError("DHW shouldn't change: {self._dhw} to {dhw}")

        if self._dhw is None:
            # self._gwy._get_device(xxx)
            # self.add_device(dhw.sensor)
            # self.add_device(dhw.relay)
            self._dhw = dhw

    @property
    def dhw_sensor(self) -> Device:
        return self._dhw._dhw_sensor if self._dhw else None

    @property
    def hotwater_valve(self) -> Device:
        return self._dhw._dhw_valve if self._dhw else None

    @property
    def heating_valve(self) -> Device:
        return self._dhw._htg_valve if self._dhw else None

    @property
    def schema(self) -> dict:
        # assert ATTR_DHW_SYSTEM not in super().schema  # TODO: removeme
        return {**super().schema, ATTR_DHW_SYSTEM: self.dhw.schema if self.dhw else {}}

    @property
    def params(self) -> dict:
        # assert ATTR_DHW_SYSTEM not in super().params  # TODO: removeme
        return {**super().params, ATTR_DHW_SYSTEM: self.dhw.params if self.dhw else {}}

    @property
    def status(self) -> dict:
        # assert ATTR_DHW_SYSTEM not in super().status  # TODO: removeme
        return {**super().status, ATTR_DHW_SYSTEM: self.dhw.status if self.dhw else {}}


class MultiZone:  # 0005 (+/- 000C?)
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.zones = []
        self.zone_by_idx = {}
        self.max_zones = self._gwy.config.max_zones

        self.zone_lock = Lock()
        self.zone_lock_idx = None

        self._prev_30c9 = None  # used to eavesdrop zone sensors

    def _discover(self, discover_flag=DISCOVER_ALL) -> None:
        super()._discover(discover_flag=discover_flag)

        if discover_flag & DISCOVER_SCHEMA:
            [  # 0005: find any zones + their type (RAD, UFH, VAL, MIX, ELE)
                self._send_cmd("0005", payload=f"00{zone_type}")
                for zone_type in (
                    _0005_ZONE.RAD,
                    _0005_ZONE.UFH,
                    _0005_ZONE.VAL,
                    _0005_ZONE.MIX,
                    _0005_ZONE.ELE,
                )
            ]

            # [  # 0005: find any others - as per an RFG100
            #     self._send_cmd("0005", payload=f"00{zone_type}")
            #     for zone_type in (
            #         _0005_ZONE.ALL,
            #         _0005_ZONE.ALL_SENSOR,
            #         "0C",  # ???
            #         _0005_ZONE.HTG,
            #         "10",  # ???
            #     )
            # ]

        # if discover_flag & DISCOVER_STATUS:
        #     self._send_cmd("0006")  # schedule delta

    def _handle_msg(self, msg, prev_msg=None):
        def find_zone_sensors(this_30c9, prev_30c9) -> None:
            """Determine each zone's sensor by matching zone/sensor temperatures.

            The temperature of each zone is reliably known (30C9 array), but the sensor
            for each zone is not. In particular, the controller may be a sensor for a
            zone, but unfortunately it does not announce its sensor temperatures.

            In addition, there may be 'orphan' (e.g. from a neighbour) sensors
            announcing temperatures with the same value.

            This leaves only a process of exclusion as a means to determine which zone
            uses the controller as a sensor.
            """

            def match_sensors(testable_sensors, zone_idx, zone_temp) -> list:
                return [
                    s
                    for s in testable_sensors
                    if s.temperature == zone_temp
                    and (s.zone is None or s.zone.idx == zone_idx)
                ]

            def _testable_zones(changed_zones) -> dict:
                return {
                    z: t
                    for z, t in changed_zones.items()
                    if self.zone_by_idx[z].sensor is None
                    # and t is not None  # done in changed_zones = {}
                    and t not in [t2 for z2, t2 in changed_zones.items() if z2 != z]
                }  # zones with unique (non-null) temps, and no sensor

            if prev_30c9 is None:
                return

            if len([z for z in self.zones if z.sensor is None]) == 0:
                return  # (currently) no zone without a sensor

            # TODO: use msgz/I, not RP
            secs = self._get_msg_value("1F09", "remaining_seconds")
            if secs is None or this_30c9.dtm > prev_30c9.dtm + td(seconds=secs + 5):
                return  # can only compare against 30C9 pkt from the last cycle

            _LOGGER.debug("System state (before): %s", self.schema)

            changed_zones = {
                z["zone_idx"]: z["temperature"]
                for z in this_30c9.payload
                if z not in prev_30c9.payload and z["temperature"] is not None
            }  # zones with changed temps
            _LOGGER.debug("Changed zones (from 30C9): %s", changed_zones)
            if not changed_zones:
                return  # ctl's 30C9 says no zones have changed temps during this cycle

            testable_zones = _testable_zones(changed_zones)
            _LOGGER.debug(
                " - has unique/non-null temps (from 30C9) & no sensor (from state): %s",
                testable_zones,
            )
            if not testable_zones:
                return  # no testable zones

            testable_sensors = [
                d
                for d in self._gwy.devices  # NOTE: *not* self._ctl.devices
                if d._ctl in (self._ctl, None)
                and d.addr.type in DEVICE_HAS_ZONE_SENSOR
                and d.temperature is not None
                and d._msgs["30C9"].dtm > prev_30c9.dtm  # changed during last cycle
            ]

            if _LOGGER.isEnabledFor(logging.DEBUG):
                _LOGGER.debug(
                    "Testable zones: %s (unique/non-null temps & sensorless)",
                    testable_zones,
                )
                _LOGGER.debug(
                    "Testable sensors: %s (non-null temps & orphans or zoneless)",
                    {d.id: d.temperature for d in testable_sensors},
                )

            if testable_sensors:  # the main matching algorithm...
                for zone_idx, temp in testable_zones.items():
                    # TODO: when sensors announce temp, ?also includes it's parent zone
                    matching_sensors = match_sensors(testable_sensors, zone_idx, temp)
                    _LOGGER.debug("Testing zone %s, temp: %s", zone_idx, temp)
                    _LOGGER.debug(
                        " - matching sensor(s): %s (same temp & not from another zone)",
                        [s.id for s in matching_sensors],
                    )

                    if len(matching_sensors) == 1:
                        _LOGGER.debug("   - matched sensor: %s", matching_sensors[0].id)
                        zone = self.zone_by_idx[zone_idx]
                        zone._set_sensor(matching_sensors[0])
                        zone.sensor._set_ctl(self._ctl)
                    elif len(matching_sensors) == 0:
                        _LOGGER.debug("   - no matching sensor (uses CTL?)")
                    else:
                        _LOGGER.debug("   - multiple sensors: %s", matching_sensors)

                _LOGGER.debug("System state (after): %s", self.schema)

            # now see if we can allocate the controller as a sensor...
            if any(z for z in self.zones if z.sensor is self._ctl):
                return  # the controller is already a sensor
            if len([z for z in self.zones if z.sensor is None]) != 1:
                return  # no single zone without a sensor

            remaining_zones = _testable_zones(changed_zones)
            if not remaining_zones:
                return  # no testable zones

            zone_idx, temp = list(remaining_zones.items())[0]
            _LOGGER.debug("Testing (sole remaining) zone %s, temp: %s", zone_idx, temp)
            # want to avoid complexity of z._temp
            # zone = self.zone_by_idx[zone_idx]
            # if zone._temp is None:
            #     return  # TODO: should have a (not-None) temperature

            matching_sensors = match_sensors(testable_sensors, zone_idx, temp)
            _LOGGER.debug(
                " - matching sensor(s): %s (excl. controller)",
                [s.id for s in matching_sensors],
            )

            # can safely(?) assume this zone is using the CTL as a sensor...
            if len(matching_sensors) == 0:
                _LOGGER.debug("   - assumed sensor: %s (by exclusion)", self._ctl.id)
                zone = self.zone_by_idx[zone_idx]
                zone._set_sensor(self._ctl)
                zone.sensor._set_ctl(self._ctl)

            _LOGGER.debug("System state (finally): %s", self.schema)

        super()._handle_msg(msg)

        if msg.code == "000A" and isinstance(msg.payload, list):
            pass
            # for zone_idx in self.zone_by_idx:
            #     cmd = Command.get_zone_mode(self.id, zone_idx, priority=Priority.LOW)
            #     self._gwy.send_cmd(cmd)
            # for zone in self.zones:
            #     zone._discover(discover_flag=DISCOVER_PARAMS)

        # elif msg.code == "0005" and prev_30c9 is not None:
        #     zone_added = bool(prev_30c9.code == "0004")  # else zone_deleted

        elif msg.code == "30C9" and isinstance(msg.payload, list):  # msg.is_array:
            if self._gwy.config.enable_eavesdrop:
                find_zone_sensors(msg, self._prev_30c9)
                self._prev_30c9 = msg

    def _get_zone(self, zone_idx, **kwargs) -> Zone:
        """Return a heating zone (will create/update it if required)."""

        # NOTE: kwargs not passed, so discovery is as eavesdropping
        zone = self.zone_by_idx.get(zone_idx) or create_zone(self, zone_idx)

        if kwargs.get("zone_type"):
            zone._set_zone_type(kwargs["zone_type"])

        if kwargs.get("sensor"):
            zone._set_sensor(kwargs["sensor"])

        if kwargs.get("actuators"):  # TODO: check not an address before implementing
            for device in [d for d in kwargs["actuators"] if d not in zone.devices]:
                device._set_parent(zone)

        return zone

    @property
    def _zones(self) -> dict:
        return sorted(self.zones, key=lambda x: x.idx)

    @property
    def schema(self) -> dict:
        # assert ATTR_ZONES not in super().schema  # TODO: removeme
        return {**super().schema, ATTR_ZONES: {z.idx: z.schema for z in self._zones}}

    @property
    def params(self) -> dict:
        # assert ATTR_ZONES not in super().params  # TODO: removeme
        return {**super().params, ATTR_ZONES: {z.idx: z.params for z in self._zones}}

    @property
    def status(self) -> dict:
        # assert ATTR_ZONES not in super().status  # TODO: removeme
        return {**super().status, ATTR_ZONES: {z.idx: z.status for z in self._zones}}


class UfhSystem:
    @property
    def schema(self) -> dict:
        # assert ATTR_UFH_SYSTEM not in super().schema  # TODO: removeme
        return {
            **super().schema,
            ATTR_UFH_SYSTEM: {
                d.id: d.schema for d in sorted(self._ctl.devices) if d.type == "02"
            },
        }

    @property
    def params(self) -> dict:
        # assert ATTR_UFH_SYSTEM not in super().params  # TODO: removeme
        return {
            **super().params,
            ATTR_UFH_SYSTEM: {
                d.id: d.params for d in sorted(self._ctl.devices) if d.type == "02"
            },
        }

    @property
    def status(self) -> dict:
        # assert ATTR_UFH_SYSTEM not in super().status  # TODO: removeme
        return {
            **super().status,
            ATTR_UFH_SYSTEM: {
                d.id: d.status for d in sorted(self._ctl.devices) if d.type == "02"
            },
        }


class SystemBase(Entity):  # 3B00 (multi-relay)
    """The most basic controllers - a generic controller (e.g. ST9420C)."""

    # 0008|0009|1030|1100|2309|3B00

    def __init__(self, gwy, ctl) -> None:
        _LOGGER.debug("Creating a System: %s (%s)", ctl.id, self.__class__)
        super().__init__(gwy)

        self.id = ctl.id
        if self.id in gwy.system_by_id:
            raise LookupError(f"Duplicate controller: {self.id}")

        gwy.system_by_id[self.id] = self
        gwy.systems.append(self)
        if gwy.evo is None:
            gwy.evo = self

        self._ctl = ctl
        self._evo = self
        self._domain_id = "FF"

        self._heat_demand = None
        self._htg_control = None

    def __repr__(self) -> str:
        return f"{self._ctl.id} (sys_base)"

    # def __str__(self) -> str:  # TODO: WIP
    #     return json.dumps({self._ctl.id: self.schema})

    def _discover(self, discover_flag=DISCOVER_ALL) -> None:
        # super()._discover(discover_flag=discover_flag)

        if discover_flag & DISCOVER_SCHEMA:
            [  # 000C: find the HTG (relay) and DHW (sensor), if any (DHW relays in DHW)
                self._send_cmd("000C", payload=f"00{dev_type}")
                for dev_type in (_000C_DEVICE.HTG, _000C_DEVICE.DHW_SENSOR)
            ]

        if discover_flag & DISCOVER_PARAMS:
            # self._send_cmd("1100", payload="FC")  # TPI params
            self._gwy.send_cmd(Command.get_tpi_params(self.id), period=td(hours=4))

        # # for code in ("3B00",):  # 3EF0, 3EF1
        # #     for payload in ("0000", "00", "F8", "F9", "FA", "FB", "FC", "FF"):
        # #         self._send_cmd(code, payload=payload)

        # # TODO: opentherm: 1FD4, 22D9, 3220

        # if discover_flag & DISCOVER_PARAMS:
        #     for domain_id in range(0xF8, 0x100):
        #         self._send_cmd("0009", payload=f"{domain_id:02X}00")

        if discover_flag & DISCOVER_STATUS:
            # for domain_id in range(0xF8, 0x100):
            #     self._send_cmd("0008", payload=f"{domain_id:02X}00")
            pass

    def _handle_msg(self, msg, prev_msg=None):
        def find_htg_control(this, prev=None):
            """Discover the heat relay (10: or 13:) for this system.

            There's' 3 ways to find a controller's heat relay (in order of reliability):
            1.  The 3220 RQ/RP *to/from a 10:* (1x/5min)
            2a. The 3EF0 RQ/RP *to/from a 10:* (1x/1min)
            2b. The 3EF0 RQ (no RP) *to a 13:* (3x/60min)
            3.  The 3B00 I/I exchange between a CTL & a 13: (TPI cycle rate, usu. 6x/hr)

            Data from the CTL is considered 'authorative'. The 1FC9 RQ/RP exchange
            to/from a CTL is too rare to be useful.
            """

            # 18:14:14.025 066 RQ --- 01:078710 10:067219 --:------ 3220 005 0000050000
            # 18:14:14.446 065 RP --- 10:067219 01:078710 --:------ 3220 005 00C00500FF
            # 14:41:46.599 064 RQ --- 01:078710 10:067219 --:------ 3EF0 001 00
            # 14:41:46.631 063 RP --- 10:067219 01:078710 --:------ 3EF0 006 0000100000FF  # noqa

            # 06:49:03.465 045 RQ --- 01:145038 13:237335 --:------ 3EF0 001 00
            # 06:49:05.467 045 RQ --- 01:145038 13:237335 --:------ 3EF0 001 00
            # 06:49:07.468 045 RQ --- 01:145038 13:237335 --:------ 3EF0 001 00
            # 09:03:59.693 051  I --- 13:237335 --:------ 13:237335 3B00 002 00C8
            # 09:04:02.667 045  I --- 01:145038 --:------ 01:145038 3B00 002 FCC8

            # note the order: most to least reliable
            heater = None

            if this.code == "3220" and this.verb == RQ:
                if this.src is self._ctl and this.dst.type == "10":
                    heater = this.dst

            elif this.code == "3EF0" and this.verb == RQ:
                if this.src is self._ctl and this.dst.type in ("10", "13"):
                    heater = this.dst

            elif this.code == "3B00" and this.verb == I_ and prev is not None:
                if this.src is self._ctl and prev.src.type == "13":
                    if prev.code == this.code and prev.verb == this.verb:
                        heater = prev.src

            if heater is not None:
                self._set_htg_control(heater)

        super()._handle_msg(msg)

        if msg.code in ("000A", "2309", "30C9") and not isinstance(msg.payload, list):
            pass
        else:
            super()._handle_msg(msg)

        if msg.code == "0008" and msg.verb in (I_, RP):
            if "domain_id" in msg.payload:
                self._relay_demands[msg.payload["domain_id"]] = msg
                if msg.payload["domain_id"] == "F9":
                    device = self.dhw.heating_valve if self.dhw else None
                elif msg.payload["domain_id"] == "FA":
                    device = self.dhw.hotwater_valve if self.dhw else None
                elif msg.payload["domain_id"] == "FC":
                    device = self.heating_control
                else:
                    device = None

                if False and device is not None:  # TODO: FIXME
                    qos = {"priority": Priority.LOW, "retries": 2}
                    for code in ("0008", "3EF1"):
                        device._send_cmd(code, qos)

        if msg.code == "3150" and msg.verb in (I_, RP):
            if "domain_id" in msg.payload and msg.payload["domain_id"] == "FC":
                self._heat_demand = msg.payload

        if msg.code in ("3220", "3B00", "3EF0"):  # self.heating_control is None and
            if self._gwy.config.enable_eavesdrop:
                find_htg_control(msg, prev=prev_msg)

    def _send_cmd(self, code, **kwargs) -> None:
        dest = kwargs.pop("dest_addr", self._ctl.id)
        payload = kwargs.pop("payload", "00")
        super()._send_cmd(code, dest, payload, **kwargs)

    @property
    def devices(self) -> List[Device]:
        return self._ctl.devices + [self._ctl]  # TODO: to sort out

    @property
    def heating_control(self) -> Device:
        if self._htg_control:
            return self._htg_control
        htg_control = [d for d in self._ctl.devices if d._domain_id == "FC"]
        return htg_control[0] if len(htg_control) == 1 else None  # HACK for 10:

    def _set_htg_control(self, device: Device) -> None:  # self._htg_control
        """Set the heating control relay for this system (10: or 13:)."""

        if self._htg_control is device:
            return
        if self._htg_control is not None:
            raise CorruptStateError(
                f"{self} changed {ATTR_HTG_CONTROL}: {self._htg_control} to {device}"
            )

        if not isinstance(device, (BdrSwitch, OtbGateway)):
            raise TypeError(f"{self}: {ATTR_HTG_CONTROL} can't be {device}")

        self._htg_control = device
        device._set_parent(self, domain="FC")  # TODO: _set_domain()

    @property
    def tpi_params(self) -> Optional[float]:  # 1100
        return self._get_msg_value("1100")

    @property
    def heat_demand(self) -> Optional[float]:  # 3150/FC
        if self._heat_demand:
            return self._heat_demand["heat_demand"]

    @property
    def is_calling_for_heat(self) -> Optional[bool]:
        """Return True is the system is currently calling for heat."""
        if not self._htg_control:
            return

        if self._htg_control.actuator_state:
            return True

    @property
    def schema(self) -> dict:
        """Return the system's schema."""

        schema = {ATTR_CONTROLLER: self._ctl.id, ATTR_HTG_SYSTEM: {}}
        # assert ATTR_HTG_SYSTEM in schema  # TODO: removeme

        # assert ATTR_HTG_CONTROL not in schema[ATTR_HTG_SYSTEM]  # TODO: removeme
        schema[ATTR_HTG_SYSTEM][ATTR_HTG_CONTROL] = (
            self.heating_control.id if self.heating_control else None
        )

        # assert ATTR_ORPHANS not in schema[ATTR_HTG_SYSTEM]  # TODO: removeme
        schema[ATTR_ORPHANS] = sorted(
            [
                d.id
                for d in self._ctl.devices
                if not d._domain_id and d.type != "02" and d._is_present
            ]
        )  # devices without a parent zone, NB: CTL can be a sensor for a zone

        # TODO: where to put this?
        # assert "devices" not in schema  # TODO: removeme
        # schema["devices"] = {d.id: d.device_info for d in sorted(self._ctl.devices)}

        return schema

    @property
    def params(self) -> dict:
        """Return the system's configuration."""

        params = {ATTR_HTG_SYSTEM: {}}
        # assert ATTR_HTG_SYSTEM in params  # TODO: removeme

        # devices don't have params
        # assert ATTR_HTG_CONTROL not in params[ATTR_HTG_SYSTEM]  # TODO: removeme
        # params[ATTR_HTG_SYSTEM][ATTR_HTG_CONTROL] = (
        #     self.heating_control.params if self.heating_control else None
        # )

        # assert "tpi_params" not in params[ATTR_HTG_SYSTEM]  # TODO: removeme
        params[ATTR_HTG_SYSTEM]["tpi_params"] = (
            self.heating_control._get_msg_value("1100")
            if self.heating_control
            else None
        )

        return params

    @property
    def status(self) -> dict:
        """Return the system's current state."""

        status = {ATTR_HTG_SYSTEM: {}}
        # assert ATTR_HTG_SYSTEM in status  # TODO: removeme

        # assert ATTR_HTG_CONTROL not in status[ATTR_HTG_SYSTEM]  # TODO: removeme
        # status[ATTR_HTG_SYSTEM][ATTR_HTG_CONTROL] = (
        #     self.heating_control.status if self.heating_control else None
        # )

        status[ATTR_HTG_SYSTEM]["heat_demand"] = self.heat_demand

        status[ATTR_DEVICES] = {d.id: d.status for d in sorted(self._ctl.devices)}

        return status


class System(StoredHw, SysDatetime, SystemBase):  # , SysFaultLog
    """The Controller class."""

    __sys_class__ = SYSTEM_CLASS.PRG

    def __init__(self, gwy, ctl, **kwargs) -> None:
        super().__init__(gwy, ctl, **kwargs)

        self._heat_demands = {}
        self._relay_demands = {}
        self._relay_failsafes = {}

    def __repr__(self) -> str:
        return f"{self._ctl.id} (system)"

    def _handle_msg(self, msg) -> bool:
        super()._handle_msg(msg)

        if "domain_id" in msg.payload:
            idx = msg.payload["domain_id"]
            if msg.code == "0008":
                self._relay_demands[idx] = msg
            elif msg.code == "0009":
                self._relay_failsafes[idx] = msg
            elif msg.code == "3150":
                self._heat_demands[idx] = msg
            elif msg.code not in ("0001", "000C", "0418", "1100", "3B00"):
                assert False, msg.code

    @property
    def heat_demands(self) -> Optional[dict]:  # 3150
        if self._heat_demands:
            return {k: v.payload["heat_demand"] for k, v in self._heat_demands.items()}

    @property
    def relay_demands(self) -> Optional[dict]:  # 0008
        if self._relay_demands:
            return {
                k: v.payload["relay_demand"] for k, v in self._relay_demands.items()
            }

    @property
    def relay_failsafes(self) -> Optional[dict]:  # 0009
        if self._relay_failsafes:
            return {}  # failsafe_enabled

    @property
    def status(self) -> dict:
        """Return the system's current state."""

        status = super().status
        # assert ATTR_HTG_SYSTEM in status  # TODO: removeme

        status[ATTR_HTG_SYSTEM]["heat_demands"] = self.heat_demands
        status[ATTR_HTG_SYSTEM]["relay_demands"] = self.relay_demands
        status[ATTR_HTG_SYSTEM]["relay_failsafes"] = self.relay_failsafes

        return status


class Evohome(SysLanguage, SysMode, MultiZone, UfhSystem, System):  # evohome
    """The Evohome system - some controllers are evohome-compatible."""

    __sys_class__ = SYSTEM_CLASS.EVO

    def __init__(self, gwy, ctl, **kwargs) -> None:
        super().__init__(gwy, ctl, **kwargs)

    def __repr__(self) -> str:
        return f"{self._ctl.id} (evohome)"

    def _discover(self, discover_flag=DISCOVER_ALL) -> None:
        super()._discover(discover_flag=discover_flag)

        if discover_flag & DISCOVER_STATUS:
            self._send_cmd("1F09")

    def _handle_msg(self, msg) -> bool:
        super()._handle_msg(msg)

        # def xxx(zone_dict):
        #     zone = self.zone_by_idx[zone_dict.pop("zone_idx")]
        #     if msg.code == "000A":
        #         zone._zone_config = zone_dict
        #     elif msg.code == "2309":
        #         zone._temp = zone_dict
        #     elif msg.code == "30C9":
        #         zone._temp = zone_dict

        # if msg.code in ("000A", "2309", "30C9"):
        #     if isinstance(msg.payload, list):
        #         super()._handle_msg(msg)
        #         [xxx(z) for z in msg.payload]
        #     else:
        #         xxx(msg.payload)

        if msg.code in ("000A", "2309", "30C9") and isinstance(msg.payload, list):
            pass


class Chronotherm(Evohome):

    __sys_class__ = SYSTEM_CLASS.EVO

    def __repr__(self) -> str:
        return f"{self._ctl.id} (chronotherm)"


class Hometronics(System):

    __sys_class__ = SYSTEM_CLASS.EVO

    RQ_SUPPORTED = ("0004", "000C", "2E04", "313F")  # TODO: WIP
    RQ_UNSUPPORTED = ("xxxx",)  # 10E0?

    def __repr__(self) -> str:
        return f"{self._ctl.id} (hometronics)"

    def _discover(self, discover_flag=DISCOVER_ALL) -> None:
        # super()._discover(discover_flag=discover_flag)

        # will RP to: 0005/configured_zones_alt, but not: configured_zones
        # will RP to: 0004

        if discover_flag & DISCOVER_STATUS:
            self._send_cmd("1F09")


class Programmer(Evohome):

    __sys_class__ = SYSTEM_CLASS.PRG

    def __repr__(self) -> str:
        return f"{self._ctl.id} (programmer)"


class Sundial(Evohome):

    __sys_class__ = SYSTEM_CLASS.PRG

    def __repr__(self) -> str:
        return f"{self._ctl.id} (sundial)"


_SYS_CLASS = {
    SystemType.CHRONOTHERM: Chronotherm,
    SystemType.EVOHOME: Evohome,
    SystemType.HOMETRONICS: Hometronics,
    SystemType.PROGRAMMER: Programmer,
    SystemType.SUNDIAL: Sundial,
    SystemType.GENERIC: System,
}
_SYS_CLASS_BY_TYPE = {
    "01": Evohome,
    "23": Programmer,
    "12": Sundial,
}


CLASS_ATTR = "__sys_class__"
SYSTEM_BY_PROFILE = {
    getattr(c[1], CLASS_ATTR): c[1]
    for c in getmembers(
        modules[__name__],
        lambda m: isclass(m) and m.__module__ == __name__ and hasattr(m, CLASS_ATTR),
    )
}  # e.g. "evohome": Evohome


def create_system(gwy, ctl, profile=None, **kwargs) -> System:
    """Create a system, and optionally perform discovery & start polling."""

    if profile is None:
        profile = SYSTEM_CLASS.PRG if ctl.type == "23" else SYSTEM_CLASS.EVO

    system = _SYS_CLASS.get(profile, System)(gwy, ctl, **kwargs)

    if not gwy.config.disable_discovery:
        system._discover(discover_flag=DISCOVER_ALL)

    return system
