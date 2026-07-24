"""HVAC room load helpers for RTSM and CLTD calculations.

The formulas in this module keep infiltration and ventilation as separate
components so system type can determine which loads are allowed to affect the
room load, total supply airflow, and chilled/hot-water flow.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

SystemType = Literal["VAV", "CAV", "OTHER"]
Method = Literal["RTSM", "CLTD"]

VAV_CAV_SYSTEMS = {"VAV", "CAV"}
SENSIBLE_AIR_LOAD_FACTOR = 1.08  # Btu/h per CFM per deg F, standard air
LATENT_AIR_LOAD_FACTOR = 0.68  # Btu/h per CFM per grain/lb
WATER_LOAD_FACTOR = 500.0  # Btu/h per GPM per deg F


@dataclass(frozen=True)
class SpaceParameters:
    """Inputs common to RTSM and CLTD room load calculations."""

    area_ft2: float
    volume_ft3: float
    occupants: float
    space_ach: float
    outdoor_air_cfm_per_person: float
    outdoor_air_cfm_per_ft2: float
    occupant_sensible_btu_h: float
    occupant_latent_btu_h: float
    indoor_temp_f: float
    outdoor_temp_f: float
    indoor_grains_lb: float = 55.0
    outdoor_grains_lb: float = 75.0


@dataclass(frozen=True)
class BaseLoads:
    """Method-specific envelope/equipment loads before outdoor-air additions."""

    sensible_cooling_btu_h: float
    latent_cooling_btu_h: float
    heating_btu_h: float


@dataclass(frozen=True)
class LoadResult:
    method: Method
    system_type: SystemType
    infiltration_cfm: float
    ventilation_cfm: float
    infiltration_sensible_btu_h: float
    infiltration_latent_btu_h: float
    ventilation_sensible_btu_h: float
    ventilation_latent_btu_h: float
    occupant_sensible_btu_h: float
    occupant_latent_btu_h: float
    room_cooling_btu_h: float
    room_heating_btu_h: float
    separate_ventilation_cooling_btu_h: float
    separate_ventilation_heating_btu_h: float
    total_cfm: float
    gpm: float


def infiltration_cfm(volume_ft3: float, space_ach: float) -> float:
    """Calculate infiltration airflow from Space Air Changes per Hour."""

    return max(volume_ft3, 0.0) * max(space_ach, 0.0) / 60.0


def ventilation_cfm(area_ft2: float, occupants: float, cfm_per_person: float, cfm_per_ft2: float) -> float:
    """Calculate required outdoor air from people and area components."""

    people_air = max(occupants, 0.0) * max(cfm_per_person, 0.0)
    area_air = max(area_ft2, 0.0) * max(cfm_per_ft2, 0.0)
    return people_air + area_air


def _air_loads(cfm: float, dry_bulb_delta_f: float, grains_delta: float) -> tuple[float, float, float]:
    sensible = SENSIBLE_AIR_LOAD_FACTOR * cfm * abs(dry_bulb_delta_f)
    latent = LATENT_AIR_LOAD_FACTOR * cfm * max(grains_delta, 0.0)
    heating = SENSIBLE_AIR_LOAD_FACTOR * cfm * max(-dry_bulb_delta_f, 0.0)
    return sensible, latent, heating


def calculate_room_loads(
    method: Method,
    system_type: SystemType,
    space: SpaceParameters,
    base_loads: BaseLoads,
    supply_air_delta_t_f: float,
    water_delta_t_f: float,
) -> LoadResult:
    """Calculate RTSM or CLTD room loads with system-specific outdoor-air logic.

    VAV/CAV systems include both infiltration and ventilation loads in room
    cooling/heating, Total CFM, and GPM. Other system types include only
    infiltration in the room load and report ventilation separately.
    """

    normalized_system = system_type.upper()
    if normalized_system not in VAV_CAV_SYSTEMS:
        normalized_system = "OTHER"

    inf_cfm = infiltration_cfm(space.volume_ft3, space.space_ach)
    vent_cfm = ventilation_cfm(
        space.area_ft2,
        space.occupants,
        space.outdoor_air_cfm_per_person,
        space.outdoor_air_cfm_per_ft2,
    )

    dry_bulb_delta = space.outdoor_temp_f - space.indoor_temp_f
    grains_delta = space.outdoor_grains_lb - space.indoor_grains_lb

    inf_sensible, inf_latent, inf_heat = _air_loads(inf_cfm, dry_bulb_delta, grains_delta)
    vent_sensible, vent_latent, vent_heat = _air_loads(vent_cfm, dry_bulb_delta, grains_delta)

    occupant_sensible = max(space.occupants, 0.0) * max(space.occupant_sensible_btu_h, 0.0)
    occupant_latent = max(space.occupants, 0.0) * max(space.occupant_latent_btu_h, 0.0)

    include_ventilation_in_room = normalized_system in VAV_CAV_SYSTEMS
    room_vent_cooling = vent_sensible + vent_latent if include_ventilation_in_room else 0.0
    room_vent_heating = vent_heat if include_ventilation_in_room else 0.0

    room_cooling = (
        base_loads.sensible_cooling_btu_h
        + base_loads.latent_cooling_btu_h
        + occupant_sensible
        + occupant_latent
        + inf_sensible
        + inf_latent
        + room_vent_cooling
    )
    room_heating = base_loads.heating_btu_h + inf_heat + room_vent_heating

    total_cfm = room_cooling / (SENSIBLE_AIR_LOAD_FACTOR * max(supply_air_delta_t_f, 0.01))
    gpm = room_cooling / (WATER_LOAD_FACTOR * max(water_delta_t_f, 0.01))

    separate_vent_cooling = 0.0 if include_ventilation_in_room else vent_sensible + vent_latent
    separate_vent_heating = 0.0 if include_ventilation_in_room else vent_heat

    return LoadResult(
        method=method,
        system_type=normalized_system,  # type: ignore[arg-type]
        infiltration_cfm=inf_cfm,
        ventilation_cfm=vent_cfm,
        infiltration_sensible_btu_h=inf_sensible,
        infiltration_latent_btu_h=inf_latent,
        ventilation_sensible_btu_h=vent_sensible,
        ventilation_latent_btu_h=vent_latent,
        occupant_sensible_btu_h=occupant_sensible,
        occupant_latent_btu_h=occupant_latent,
        room_cooling_btu_h=room_cooling,
        room_heating_btu_h=room_heating,
        separate_ventilation_cooling_btu_h=separate_vent_cooling,
        separate_ventilation_heating_btu_h=separate_vent_heating,
        total_cfm=total_cfm,
        gpm=gpm,
    )
