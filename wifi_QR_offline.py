# ساخته شده توسط امیرحسین شیری
# برنامه تشخیص رمز وای فای با بارکد آن

import argparse
import os
import re

from PIL import Image
from pyzbar.pyzbar import decode


argparser = argparse.ArgumentParser(
    "wifi_qr_offline", "برنامه تشخیص رمز وای فای با بارکد آن"
)

argparser.add_argument("image_path")


# الگوی وای‌فای
WIFI_RE = re.compile(r"WIFI:(\w:.+;)+", re.IGNORECASE)

# الگوی ویژگی های وای‌فای
WIFI_PROPERTY_RE = re.compile(r"(\w):([^;]*);")

# نام های کامل ویژگی های وای‌فای
WIFI_PROPERTIES = {
    "H": "Hidden Network",
    "P": "Password",
    "S": "SSID",
    "T": "Authentication Type",
}


def read_qr_offline():
    """خواندن QR از تصویر و استخراج SSID و Password در صورت وجود."""

    image_path = argparser.parse_args().image_path

    # بررسی وجود فایل
    if not os.path.exists(image_path):
        print(" فایل پیدا نشد:", image_path)
        return None

    try:
        img = Image.open(image_path)
    except Exception as e:
        print(" خطا در باز کردن تصویر:", e)
        return None

    decoded = decode(img)

    if not decoded:
        print(" هیچ کد QR در عکس پیدا نشد.")
        return None

    for obj in decoded:
        qr_text = obj.data.decode("utf-8")
        print(" متن QR شناسایی‌شده:")
        print(qr_text)

        # بررسی فرمت وای‌فای
        m = WIFI_RE.search(qr_text)
        if m:
            print("\n وای‌فای شناسایی شد:")
            matches = WIFI_PROPERTY_RE.findall(m.group(1))
            for match in matches:
                print(f"{WIFI_PROPERTIES.get(match[0]) or match[0]}: {match[1]}")
        else:
            print("\nاین QR مربوط به وای‌فای نیست یا فرمتش متفاوت است.")
            return None


if __name__ == "__main__":
    read_qr_offline()
