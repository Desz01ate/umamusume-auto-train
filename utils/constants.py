from utils.resolution import scale_relative_region

# Relative coordinates (0.0-1.0) based on 1920x1080 reference resolution
SUPPORT_CARD_ICON_REGION_REL = (0.440, 0.144, 0.052, 0.505)  # (845, 155, 100, 545)
MOOD_REGION_REL = (0.367, 0.116, 0.068, 0.023)  # (705, 125, 130, 25)
TURN_REGION_REL = (0.135, 0.060, 0.057, 0.069)  # (260, 65, 110, 75)
FAILURE_REGION_REL = (0.130, 0.713, 0.292, 0.060)  # (250, 770, 560, 65)
YEAR_REGION_REL = (0.133, 0.032, 0.086, 0.023)  # (255, 35, 165, 25)
CRITERIA_REGION_REL = (0.237, 0.079, 0.089, 0.028)  # (455, 85, 170, 30)
SKILL_PTS_REGION_REL = (0.396, 0.722, 0.034, 0.032)  # (760, 780, 65, 35)

MOOD_LIST = ["AWFUL", "BAD", "NORMAL", "GOOD", "GREAT", "UNKNOWN"]

# Functions to get scaled regions
def get_support_card_icon_region():
    return scale_relative_region(SUPPORT_CARD_ICON_REGION_REL)

def get_mood_region():
    return scale_relative_region(MOOD_REGION_REL)

def get_turn_region():
    return scale_relative_region(TURN_REGION_REL)

def get_failure_region():
    return scale_relative_region(FAILURE_REGION_REL)

def get_year_region():
    return scale_relative_region(YEAR_REGION_REL)

def get_criteria_region():
    return scale_relative_region(CRITERIA_REGION_REL)

def get_skill_pts_region():
    return scale_relative_region(SKILL_PTS_REGION_REL)

# Legacy constants for backward compatibility (deprecated)
SUPPORT_CARD_ICON_REGION = get_support_card_icon_region()
MOOD_REGION = get_mood_region()
TURN_REGION = get_turn_region()
FAILURE_REGION = get_failure_region()
YEAR_REGION = get_year_region()
CRITERIA_REGION = get_criteria_region()
SKILL_PTS_REGION = get_skill_pts_region()