"""Space type defaults based on ASHRAE 62.1 outdoor-air rate structure.

Values are IP units: CFM/person for occupant outdoor air and CFM/ft² for area
outdoor air. Projects should verify the applicable ASHRAE 62.1 edition and
local amendments before final design.
"""

SPACE_TYPES = {
    "office": {"cfm_per_person": 5.0, "cfm_per_ft2": 0.06, "occupant_latent_btu_h": 200.0},
    "conference_meeting": {"cfm_per_person": 5.0, "cfm_per_ft2": 0.06, "occupant_latent_btu_h": 205.0},
    "classroom_ages_9_plus": {"cfm_per_person": 10.0, "cfm_per_ft2": 0.12, "occupant_latent_btu_h": 205.0},
    "lecture_classroom": {"cfm_per_person": 7.5, "cfm_per_ft2": 0.06, "occupant_latent_btu_h": 205.0},
    "retail_sales": {"cfm_per_person": 7.5, "cfm_per_ft2": 0.12, "occupant_latent_btu_h": 200.0},
    "hotel_guest_room": {"cfm_per_person": 5.0, "cfm_per_ft2": 0.06, "occupant_latent_btu_h": 180.0},
    "restaurant_dining": {"cfm_per_person": 7.5, "cfm_per_ft2": 0.18, "occupant_latent_btu_h": 255.0},
    "gym_sports_area": {"cfm_per_person": 20.0, "cfm_per_ft2": 0.18, "occupant_latent_btu_h": 525.0},
}
