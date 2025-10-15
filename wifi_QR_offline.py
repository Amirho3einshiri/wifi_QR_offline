# ساخته شده توسط امیرحسین شیری
# برنامه تشخیص رمز وای فای با بارکد آن

import argparse
import os
import re

from PIL import Image
from pyzbar.pyzbar import decode

# الگوی وای‌فای
WIFI_RE = re.compile(
    r"WIFI:S:(?P<ssid>[^;]+);P:(?P<pw>[^;]+);",
    re.IGNORECASE
)

def read_qr_offline(image_path):
    """خواندن QR از تصویر و استخراج SSID و Password در صورت وجود."""

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
            ssid = m.group("ssid")
            pw = m.group("pw")
            print("\n وای‌فای شناسایی شد:")
            print(f" SSID: {ssid}")
            print(f" Password: {pw}")
            return pw
        else:
            print("\nℹ این QR مربوط به وای‌فای نیست یا فرمتش متفاوت است.")
            return None

if __name__ == "__main__":
    read_qr_offline(IMAGE_PATH)