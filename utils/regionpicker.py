import pyautogui
import time

def get_mouse_position():
    print("Move your mouse to the desired region. Press Ctrl+C to stop.")
    try:
        while True:
            x, y = pyautogui.position()
            print(f"Mouse position: x={x}, y={y}")
            time.sleep(0.1)  # Update every 0.1 seconds
    except KeyboardInterrupt:
        print("Stopped.")

if __name__ == "__main__":
    get_mouse_position()