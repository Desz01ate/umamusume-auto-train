import time
import pygetwindow as gw
import threading
import uvicorn
import keyboard
import pyautogui

from core.execute import career_lobby
import core.state as state
from server.main import app
from utils.resolution import get_resolution_manager

hotkey = "f1"

def focus_umamusume():
  try:
    win = gw.getWindowsWithTitle("Umamusume")
    target_window = next((w for w in win if w.title.strip() == "Umamusume"), None)
    if target_window.isMinimized:
      target_window.restore()
    else:
      target_window.minimize()
      time.sleep(0.2)
      target_window.restore()
      time.sleep(0.5)
  except Exception as e:
    print(f"Error focusing window: {e}")
    return False
  return True

def main():
  print("Uma Auto!")
  if focus_umamusume():
    state.reload_config()
    career_lobby()
  else:
    print("Failed to focus Umamusume window")

def hotkey_listener():
  while True:
    keyboard.wait(hotkey)
    if not state.is_bot_running:
      print("[BOT] Starting...")
      state.is_bot_running = True
      t = threading.Thread(target=main, daemon=True)
      t.start()
    else:
      print("[BOT] Stopping...")
      state.is_bot_running = False
    time.sleep(0.5)

def start_server():
  # Initialize resolution manager and check support
  res_manager = get_resolution_manager()
  res_info = res_manager.get_resolution_info()
  
  print(f"[INFO] Detected resolution: {res_info['current_resolution'][0]}x{res_info['current_resolution'][1]}")
  print(f"[INFO] Scale factors: {res_info['scale_factors'][0]:.2f}x, {res_info['scale_factors'][1]:.2f}y")
  
  if not res_info['is_supported']:
    print(f"[WARNING] Your resolution {res_info['current_resolution'][0]}x{res_info['current_resolution'][1]} may not be fully supported.")
    print(f"[WARNING] Aspect ratio: {res_info['aspect_ratio']:.2f} (16:9 = 1.78)")
    print("[WARNING] The bot may not work correctly. Supported resolutions:")
    from utils.resolution import SUPPORTED_RESOLUTIONS
    for res in SUPPORTED_RESOLUTIONS:
      print(f"  - {res[0]}x{res[1]}")
    print("[INFO] Continuing anyway. Please report issues if the bot doesn't work properly.")
  
  host = "127.0.0.1"
  port = 8000
  print(f"[INFO] Press '{hotkey}' to start/stop the bot.")
  print(f"[SERVER] Open http://{host}:{port} to configure the bot.")
  config = uvicorn.Config(app, host=host, port=port, workers=1, log_level="warning")
  server = uvicorn.Server(config)
  server.run()

if __name__ == "__main__":
  threading.Thread(target=hotkey_listener, daemon=True).start()
  start_server()
