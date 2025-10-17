# ساخته شده توسط امیرحسین شیری
# برنامه تشخیص رمز وای فای با بارکد آن

import argparse
import os
import re
from PIL import Image
from pyzbar.pyzbar import decode

# تنظیم آرگومان خط فرمان برای دریافت مسیر عکس
argparser = argparse.ArgumentParser("wifi_qr_offline", description="برنامه تشخیص رمز وای فای با بارکد آن")
argparser.add_argument("image_path", help="مسیر تصویر QR وای‌فای")

# الگوی وای‌فای
WIFI_RE = re.compile(r"WIFI:S:(?P<ssid>[^;]+);P:(?P<pw>[^;]+);", re.IGNORECASE)

def read_qr_offline(image_path):
    """خواندن QR از تصویر و استخراج SSID و Password در صورت وجود."""

    if not os.path.exists(image_path):
        print("❌ فایل پیدا نشد:", image_path)
        return None

    try:
        img = Image.open(image_path)
    except Exception as e:
        print("❌ خطا در باز کردن تصویر:", e)
        return None

    decoded = decode(img)

    if not decoded:
        print("ℹ هیچ کد QR در عکس پیدا نشد.")
        return None

    for obj in decoded:
        qr_text = obj.data.decode("utf-8")
        print("📦 متن QR شناسایی‌شده:")
        print(qr_text)

        m = WIFI_RE.search(qr_text)
        if m:
            ssid = m.group("ssid")
            pw = m.group("pw")
            print("\n✅ وای‌فای شناسایی شد:")
            print(f"🔐 SSID: {ssid}")
            print(f"🔑 Password: {pw}")
            save_password_to_file(ssid, pw)
            return pw
        else:
            print("\nℹ این QR مربوط به وای‌فای نیست یا فرمتش متفاوت است.")
            return None

def save_password_to_file(ssid, pw, filename="wifi_password.txt"):
    """ذخیره SSID و Password در فایل متنی."""
    try:
        with open(filename, mode="w", encoding="utf-8") as f:
            f.write(f"SSID: {ssid}\nPassword: {pw}\n")
        print(f"\n📁 رمز وای‌فای در فایل '{filename}' ذخیره شد.")
    except Exception as e:
        print("❌ خطا در ذخیره‌سازی رمز:", e)

if __name__ == "__main__":
    args = argparser.parse_args()
    read_qr_offline(args.image_path)
