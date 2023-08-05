import re

from lcbuilder.objectinfo.InputObjectInfo import InputObjectInfo
from lcbuilder.objectinfo.MissionFfiCoordsObjectInfo import MissionFfiCoordsObjectInfo
from lcbuilder.objectinfo.MissionFfiIdObjectInfo import MissionFfiIdObjectInfo
from lcbuilder.objectinfo.MissionInputObjectInfo import MissionInputObjectInfo
from lcbuilder.objectinfo.MissionObjectInfo import MissionObjectInfo
from lcbuilder.objectinfo.ObjectInfo import ObjectInfo
from lcbuilder.objectinfo.preparer.MissionFfiLightcurveBuilder import MissionFfiLightcurveBuilder
from lcbuilder.objectinfo.preparer.MissionInputLightcurveBuilder import MissionInputLightcurveBuilder
from lcbuilder.objectinfo.preparer.MissionLightcurveBuilder import MissionLightcurveBuilder



class LcBuilder:
    COORDS_REGEX = "^(-{0,1}[0-9.]+)_(-{0,1}[0-9.]+)$"
    DEFAULT_CADENCES_FOR_MISSION = {"Kepler": 60, "K2": 60, "TESS": 120}

    def __init__(self) -> None:
        self.lightcurve_builders = {InputObjectInfo: MissionInputLightcurveBuilder(),
                                    MissionInputObjectInfo: MissionInputLightcurveBuilder(),
                                    MissionObjectInfo: MissionLightcurveBuilder(),
                                    MissionFfiIdObjectInfo: MissionFfiLightcurveBuilder(),
                                    MissionFfiCoordsObjectInfo: MissionFfiLightcurveBuilder()}

    def build(self, object_info: ObjectInfo, object_dir: str):
        return self.lightcurve_builders[type(object_info)].build(object_info, object_dir)

    def build_object_info(self, target_name, author, sectors, file, cadence, initial_mask, initial_transit_mask,
                          initial_detrend_period, star_info, aperture):
        mission = None
        coords = None
        try:
            mission, mission_prefix, id = MissionLightcurveBuilder().parse_object_id(target_name)
        except ValueError:
            coords = self.parse_coords(target_name)
        cadence = cadence if cadence is not None else self.DEFAULT_CADENCES_FOR_MISSION[mission]
        if mission is not None and file is None and cadence <= 300:
            return MissionObjectInfo(target_name, sectors, author, cadence, initial_mask, initial_transit_mask,
                              initial_detrend_period, star_info, aperture)
        elif mission is not None and file is None and cadence > 300:
            return MissionFfiIdObjectInfo(target_name, sectors, author, cadence, initial_mask, initial_transit_mask,
                                   initial_detrend_period, star_info, aperture)
        elif mission is not None and file is not None:
            return MissionInputObjectInfo(target_name, file, initial_mask, initial_transit_mask, initial_detrend_period,
                                   star_info, aperture)
        elif mission is None and coords is not None and cadence > 300:
            return MissionFfiCoordsObjectInfo(coords[0], coords[1], sectors, author, cadence, initial_mask,
                                       initial_transit_mask, initial_detrend_period, star_info, aperture)
        elif mission is None and file is not None:
            return InputObjectInfo(file, initial_mask, initial_transit_mask, initial_detrend_period, star_info, aperture)
        else:
            raise ValueError(
                "Invalid target definition with mission=%s, id=%s, coords=%s, sectors=%s, file=%s, cadence=%s")

    def parse_object_info(self, target: str):
        return MissionLightcurveBuilder().parse_object_id(target)

    def parse_coords(self, target: str):
        coords_parsed = re.search(self.COORDS_REGEX, target)
        coords = [coords_parsed.group(1), coords_parsed.group(2)] if coords_parsed is not None else None
        return coords
