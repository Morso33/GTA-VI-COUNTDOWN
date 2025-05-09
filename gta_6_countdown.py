from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import ctypes
import os
from PIL import Image, ImageDraw, ImageFont
import random

RELEASE_DATE = datetime(2026, 5, 26) #Change this if it gets delayed again...
SCREENSHOTS_DIR = './screenshots' 

def get_days_until_release(release_date):
    today = datetime.now()
    delta = release_date - today
    return delta.days

def get_random_screenshot(screenshots_dir):
    files = [f for f in os.listdir(screenshots_dir)
             if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        raise FileNotFoundError("No valid image files found in screenshots directory.")
    return os.path.join(screenshots_dir, random.choice(files))

def create_days_left_image(days_left, background_path):
    img = Image.open(background_path).convert("RGB")
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 200) # Font and size can be adjusted here
    except IOError:
        font = ImageFont.load_default()

    text = f"{days_left}" # You can edit this to "days left" or whatever you want

    text_bbox = d.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    img_width, img_height = img.size
    x = (img_width - text_width) // 2
    y = (img_height - text_height) // 2

    d.text((x, y), text, fill=(255, 255, 255), font=font)

    output_path = 'gta_6_countdown.png'
    img.save(output_path)
    return output_path

def set_windows_wallpaper(image_path):
    image_path = os.path.abspath(image_path)

    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x1
    SPIF_SENDCHANGE = 0x2

    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )

def main():
    days_left = get_days_until_release(RELEASE_DATE)
    background = get_random_screenshot(SCREENSHOTS_DIR)
    countdown_image = create_days_left_image(days_left, background)
    set_windows_wallpaper(countdown_image)

if __name__ == "__main__":
    main()