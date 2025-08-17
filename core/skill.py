import pyautogui
import Levenshtein

from utils.screenshot import enhanced_screenshot
from core.ocr import extract_text
from core.recognizer import match_template, is_btn_active
import core.state as state
from utils.resolution import scale_coordinate, scale_region

def buy_skill():
  # Scale the mouse position for skill selection
  scaled_x, scaled_y = scale_coordinate(560, 680)
  pyautogui.moveTo(x=scaled_x, y=scaled_y)
  found = False

  for i in range(10):
    buy_skill_icon = match_template("assets/icons/buy_skill.png", threshold=0.9)

    if buy_skill_icon:
      for x, y, w, h in buy_skill_icon:
        # Scale the region for skill text detection
        region = scale_region((x - 420, y - 40, w + 275, h + 5))
        screenshot = enhanced_screenshot(region)
        text = extract_text(screenshot)
        if is_skill_match(text, state.SKILL_LIST):
          button_region = (x, y, w, h)
          if is_btn_active(button_region):
            print(f"[INFO] Buy {text}")
            pyautogui.click(x=x + 5, y=y + 5, duration=0.15)
            found = True
          else:
            print(f"[INFO] {text} found but not enough skill points.")

    for i in range(7):
      pyautogui.scroll(-300)

  return found

def is_skill_match(text: str, skill_list: list[str], threshold: float = 0.75) -> bool:
  for skill in skill_list:
    similarity = Levenshtein.ratio(text.lower(), skill.lower())
    if similarity >= threshold:
      return True
  return False