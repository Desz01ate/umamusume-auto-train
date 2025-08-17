import re
import json

from utils.screenshot import capture_region, enhanced_screenshot
from core.ocr import extract_text, extract_number
from core.recognizer import match_template

from utils.constants import MOOD_LIST, get_support_card_icon_region, get_mood_region, get_turn_region, get_failure_region, get_year_region, get_criteria_region, get_skill_pts_region
from utils.resolution import scale_region

is_bot_running = False

MINIMUM_MOOD = None
PRIORITIZE_G1_RACE = None
IS_AUTO_BUY_SKILL = None
SKILL_PTS_CHECK = None
PRIORITY_STAT = None
MAX_FAILURE = None
STAT_CAPS = None
SKILL_LIST = None
CANCEL_CONSECUTIVE_RACE = None

def load_config():
  with open("config.json", "r", encoding="utf-8") as file:
    return json.load(file)

def reload_config():
  global PRIORITY_STAT, MINIMUM_MOOD, MAX_FAILURE, PRIORITIZE_G1_RACE, CANCEL_CONSECUTIVE_RACE, STAT_CAPS, IS_AUTO_BUY_SKILL, SKILL_PTS_CHECK, SKILL_LIST
  config = load_config()

  PRIORITY_STAT = config["priority_stat"]
  MINIMUM_MOOD = config["minimum_mood"]
  MAX_FAILURE = config["maximum_failure"]
  PRIORITIZE_G1_RACE = config["prioritize_g1_race"]
  CANCEL_CONSECUTIVE_RACE = config["cancel_consecutive_race"]
  STAT_CAPS = config["stat_caps"]
  IS_AUTO_BUY_SKILL = config["skill"]["is_auto_buy_skill"]
  SKILL_PTS_CHECK = config["skill"]["skill_pts_check"]
  SKILL_LIST = config["skill"]["skill_list"]

# Get Stat
def stat_state():
  # Base stat regions (relative to 1920x1080)
  base_stat_regions = {
    "spd": (310, 723, 55, 20),
    "sta": (405, 723, 55, 20),
    "pwr": (500, 723, 55, 20),
    "guts": (595, 723, 55, 20),
    "wit": (690, 723, 55, 20)
  }

  result = {}
  for stat, base_region in base_stat_regions.items():
    # Scale the region for current resolution
    scaled_region = scale_region(base_region)
    img = enhanced_screenshot(scaled_region)
    val = extract_number(img)
    result[stat] = val
  return result

# Check support card in each training
def check_support_card(threshold=0.8):
  SUPPORT_ICONS = {
    "spd": "assets/icons/support_card_type_spd.png",
    "sta": "assets/icons/support_card_type_sta.png",
    "pwr": "assets/icons/support_card_type_pwr.png",
    "guts": "assets/icons/support_card_type_guts.png",
    "wit": "assets/icons/support_card_type_wit.png",
    "friend": "assets/icons/support_card_type_friend.png"
  }

  count_result = {}

  for key, icon_path in SUPPORT_ICONS.items():
    # Get the dynamically scaled support card icon region
    support_region = get_support_card_icon_region()
    matches = match_template(icon_path, support_region, threshold)
    count_result[key] = len(matches)

  return count_result

# Get failure chance (idk how to get energy value)
def check_failure():
  failure_region = get_failure_region()
  failure = enhanced_screenshot(failure_region)
  failure_text = extract_text(failure).lower()

  if not failure_text.startswith("failure"):
    return -1

  # SAFE CHECK
  # 1. If there is a %, extract the number before the %
  match_percent = re.search(r"failure\s+(\d{1,3})%", failure_text)
  if match_percent:
    return int(match_percent.group(1))

  # 2. If there is no %, but there is a 9, extract digits before the 9
  match_number = re.search(r"failure\s+(\d+)", failure_text)
  if match_number:
    digits = match_number.group(1)
    idx = digits.find("9")
    if idx > 0:
      num = digits[:idx]
      return int(num) if num.isdigit() else -1
    elif digits.isdigit():
      return int(digits)  # fallback

  return -1

# Check mood
def check_mood():
  mood_region = get_mood_region()
  mood = capture_region(mood_region)
  mood_text = extract_text(mood).upper()

  for known_mood in MOOD_LIST:
    if known_mood in mood_text:
      return known_mood

  print(f"[WARNING] Mood not recognized: {mood_text}")
  return "UNKNOWN"

# Check turn
def check_turn():
    turn_region = get_turn_region()
    turn = enhanced_screenshot(turn_region)
    turn_text = extract_text(turn)

    if "Race Day" in turn_text:
        return "Race Day"

    # sometimes easyocr misreads characters instead of numbers
    cleaned_text = (
        turn_text
        .replace("T", "1")
        .replace("I", "1")
        .replace("O", "0")
        .replace("S", "5")
    )

    digits_only = re.sub(r"[^\d]", "", cleaned_text)

    if digits_only:
      return int(digits_only)
    
    return -1

# Check year
def check_current_year():
  year_region = get_year_region()
  year = enhanced_screenshot(year_region)
  text = extract_text(year)
  return text

# Check criteria
def check_criteria():
  criteria_region = get_criteria_region()
  img = enhanced_screenshot(criteria_region)
  text = extract_text(img)
  return text

def check_skill_pts():
  skill_pts_region = get_skill_pts_region()
  img = enhanced_screenshot(skill_pts_region)
  text = extract_number(img)
  return text