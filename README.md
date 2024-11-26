# Screenshot OCR Script

This Python script captures screenshots of specific regions of your screen with a single press of the **F8** key. It processes the screenshots using Optical Character Recognition (OCR) to extract text from the images and stores the results in an SQLite database.

---

## Features
- **Automatic Screenshot Capture**: With just one press of the **F8** key, the script captures screenshots of predefined screen regions.
- **OCR Processing**: It uses Tesseract OCR to recognize text from the screenshots in both **English** and **Russian**.
- **Database Storage**: The extracted text is stored in an SQLite database for future use, with each screenshot saved in a dedicated folder named with a timestamp.
- **Customizable Regions**: The regions from which the screenshots are taken can be easily modified to match your screen layout.

## Requirements

### Operating System:
- **Windows 10**

### Dependencies:
1. **Python 3.x** (Download from [python.org](https://www.python.org/downloads/))
2. **Tesseract OCR** (Used for text recognition from the screenshots)

### How to Install and Run

### 1. Install Python
If you don't have Python installed, follow these steps:

- Download the installer for Python from [here](https://www.python.org/downloads/).
- Run the installer and follow the installation prompts. Ensure you check the box **"Add Python to PATH"** during installation.
  
### 2. Install Dependencies
After installing Python, open the Command Prompt (`cmd`) and run the following commands to install required libraries:

```bash
pip install pytesseract mss pillow pynput sqlite3 plyer
```

### 3. Install Tesseract OCR
- Download and install Tesseract OCR from [this link](https://github.com/tesseract-ocr/tesseract/wiki).
- During installation, choose the default installation path or install it in a location that is convenient for you (e.g., `C:\Program Files\Tesseract-OCR`).
- Make sure to configure the Tesseract path in the script (explained below).

### 4. Update Tesseract Path
In the script, there is a line where Tesseract's executable is configured. Make sure it points to the correct path of the Tesseract OCR executable. By default, the script uses:

```python
pytesseract.pytesseract.tesseract_cmd = os.path.join(
    os.environ['USERPROFILE'],
    "AppData",
    "Local",
    "Programs",
    "Tesseract-OCR",
    "tesseract.exe"
)
```

If your installation path differs, update the path accordingly.

### 5. Run the Script
After installing Python and the dependencies, save the provided Python script as `ocr.py` on your computer. Then, open the Command Prompt, navigate to the folder containing `ocr.py`, and run:

```bash
python ocr.py
```

### 6. Using the Script
- **Press F8** to capture the screenshots and perform OCR on the predefined regions.
- **Press Escape** to exit the script.

### What You Can Modify

1. **Regions for Screenshots**: 
   - The regions are predefined in the script. You can change the coordinates and sizes for each region to capture the areas that are relevant for your needs. Here is the format:
   ```python
   "name": (x, y, width, height)  # Example region (top-left x, top-left y, width, height)
   ```

2. **Tesseract Language**:
   - The OCR is set to recognize both English and Russian (`rus+eng` language code). If you need other languages, modify the `lang` parameter in `pytesseract.image_to_string()`:
   ```python
   extracted_text = pytesseract.image_to_string(screenshot_image, lang="eng")  # For English only
   ```

3. **Database Fields**:
   - If you want to add or remove fields from the database (e.g., adding a region for "date"), you can modify both the regions dictionary and the database schema.
   - Update the database initialization and insert queries to match your changes.

4. **Folder Structure**:
   - The script saves screenshots in a timestamped folder. If you prefer to organize screenshots differently, you can modify the `screenshots_folder` path:
   ```python
   screenshots_folder = os.path.join("your_folder_name", timestamp)
   ```

---

## Script Overview

Here is a high-level breakdown of the script:

1. **Database Initialization**:
   - Creates a database (`ocr_data.db`) and a table to store the OCR data (name, number, chat content, etc.).

2. **Screenshot and OCR**:
   - The script captures screenshots of predefined regions on the screen.
   - It saves the images to a folder named by the current timestamp.
   - It processes each screenshot using Tesseract OCR to extract text, which is then saved into the SQLite database.

3. **Hotkey Listener**:
   - The script uses the `pynput` library to listen for hotkey presses (F8 for capturing OCR, Escape for exiting).

4. **Folder Structure**:
   - Screenshots are saved in a `screenshots` folder, and each capture is stored in a subfolder named with the current timestamp.

5. **Database Storage**:
   - The recognized text from each region is stored in an SQLite database under fields like `name`, `number`, and `chat_content`.

---

## Future Improvements

1. **Dialog Notification During Region Selection**:
   - Add visual prompts or dialog boxes to guide users while selecting screen regions for OCR.

2. **Visual Region Selection**:
   - Allow users to visually select regions on the screen by clicking and dragging the mouse.

3. **Field and Region Counter Setup**:
   - Provide a counter to manage multiple fields and regions, ensuring users don't select overlapping or incorrect regions.

---

## Example Output

After pressing F8 and performing OCR, the script will display the following message:

```plaintext
Success: All regions were saved to screenshots/2024-11-28_10-30-45 and recognized.
```

And the extracted text will be stored in the database (`ocr_data.db`).

---

## License

This script is released under the [MIT License](https://opensource.org/licenses/MIT).

Feel free to modify and distribute it as per your needs.

---

### Contact

For further questions or support, please contact me at [your email/contact].

---

This `README.md` provides a detailed explanation of how to install, run, and modify the script for your specific needs.