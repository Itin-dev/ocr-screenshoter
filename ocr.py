import os
import pytesseract
import sqlite3
from datetime import datetime
from pynput import keyboard
import mss
from PIL import Image

# Configure the path to Tesseract OCR dynamically
pytesseract.pytesseract.tesseract_cmd = os.path.join(
    os.environ['USERPROFILE'],
    "AppData",
    "Local",
    "Programs",
    "Tesseract-OCR",
    "tesseract.exe"
)

# Define screen regions (x, y, width, height)
regions = {
    "name": (-1800, 35, 500, 35),              # Region 1: Name
    "number": (-1800, 75, 200, 30),            # Region 2: Number
    "chat_content": (-1914, 130, 1264, 891),      # Region 3: Chat Content
}

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("ocr_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ocr_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            folder TEXT NOT NULL,
            name TEXT,
            number TEXT,
            chat_content TEXT
        )
    """)
    conn.commit()
    return conn

# Capture screenshots, store them in a timestamped folder, and perform OCR
def take_screenshots_and_ocr():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshots_folder = os.path.join("screenshots", timestamp)
    os.makedirs(screenshots_folder, exist_ok=True)

    conn = init_db()
    cursor = conn.cursor()

    data = {"timestamp": timestamp, "folder": screenshots_folder}
    all_successful = True
    failed_regions = []

    with mss.mss() as sct:
        for field, region in regions.items():
            try:
                # Define region for mss
                x, y, width, height = region
                monitor_region = {"top": y, "left": x, "width": width, "height": height}

                # Capture the region
                screenshot = sct.grab(monitor_region)
                screenshot_image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                screenshot_path = os.path.join(screenshots_folder, f"{field}.png")
                screenshot_image.save(screenshot_path)

                # Perform OCR
                extracted_text = pytesseract.image_to_string(screenshot_image, lang="rus+eng").strip()
                if not extracted_text:
                    raise ValueError(f"No text detected for {field}")
                data[field] = extracted_text
            except Exception as e:
                all_successful = False
                failed_regions.append(f"{field}: {e}")

    if all_successful:
        cursor.execute("""
            INSERT INTO ocr_data (timestamp, folder, name, number, chat_content)
            VALUES (?, ?, ?, ?, ?)
        """, (
            timestamp,
            screenshots_folder,
            data.get("name", ""),
            data.get("number", ""),
            data.get("chat_content", "")
        ))
        conn.commit()
        print(f"Success: All regions were saved to {screenshots_folder} and recognized.")
    else:
        print(f"Error: Some regions failed to process:\n{', '.join(failed_regions)}")

    conn.close()

# Define the hotkey listener
def on_press(key):
    try:
        if key == keyboard.Key.f8:  # Use F8 as the hotkey
            print("Hotkey pressed: Taking screenshots and performing OCR...")
            take_screenshots_and_ocr()
        elif key == keyboard.Key.esc:  # Stop the program on Escape
            print("Escape pressed: Exiting program.")
            return False  # Stops the listener
    except Exception as e:
        print(f"Error with hotkey listener: {e}")

if __name__ == "__main__":
    print("Press F8 to take a screenshot pack and perform OCR. Press Escape to exit.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()