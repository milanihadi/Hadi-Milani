import unittest

from src.load_calculations import BaseLoads, SpaceParameters, calculate_room_loads
from src.space_types import SPACE_TYPES


class LoadCalculationTests(unittest.TestCase):
    def setUp(self):
        self.space = SpaceParameters(
            area_ft2=1000,
            volume_ft3=10000,
            occupants=10,
            space_ach=0.6,
            outdoor_air_cfm_per_person=5,
            outdoor_air_cfm_per_ft2=0.06,
            occupant_sensible_btu_h=245,
            occupant_latent_btu_h=200,
            indoor_temp_f=75,
            outdoor_temp_f=95,
        )
        self.base = BaseLoads(12000, 1000, 8000)

    def test_space_ach_changes_total_cfm_for_rtsm(self):
        low = calculate_room_loads("RTSM", "VAV", self.space, self.base, 20, 10)
        high_space = self.space.__class__(**{**self.space.__dict__, "space_ach": 1.2})
        high = calculate_room_loads("RTSM", "VAV", high_space, self.base, 20, 10)
        self.assertGreater(high.total_cfm, low.total_cfm)

    def test_space_ach_changes_total_cfm_for_cltd(self):
        low = calculate_room_loads("CLTD", "CAV", self.space, self.base, 20, 10)
        high_space = self.space.__class__(**{**self.space.__dict__, "space_ach": 1.2})
        high = calculate_room_loads("CLTD", "CAV", high_space, self.base, 20, 10)
        self.assertGreater(high.total_cfm, low.total_cfm)

    def test_non_vav_cav_keeps_ventilation_separate(self):
        result = calculate_room_loads("RTSM", "OTHER", self.space, self.base, 20, 10)
        self.assertGreater(result.separate_ventilation_cooling_btu_h, 0)
        vav = calculate_room_loads("RTSM", "VAV", self.space, self.base, 20, 10)
        self.assertGreater(vav.room_cooling_btu_h, result.room_cooling_btu_h)

    def test_space_type_database_includes_area_oa_and_latent(self):
        self.assertIn("cfm_per_ft2", SPACE_TYPES["office"])
        self.assertIn("occupant_latent_btu_h", SPACE_TYPES["office"])


if __name__ == "__main__":
    unittest.main()
