# ساخته شده توسط امیرحسین شیری
# برنامه تشخیص رمز وای فای با بارکد آن

import argparse
import os
import re
from datetime import datetime
from PIL import Image
from pyzbar.pyzbar import decode

# تنظیم آرگومان خط فرمان برای دریافت مسیر عکس
argparser = argparse.ArgumentParser("wifi_qr_offline", description="برنامه تشخیص رمز وای فای با بارکد آن")
argparser.add_argument("image_path", help="مسیر تصویر QR وای‌فای")


# الگوی وای‌فای
WIFI_RE = re.compile(r"WIFI:(\w:.+;)+", re.IGNORECASE)

# الگوی پارامترهای وای‌فای
WIFI_PARAMETERS_RE = re.compile(r"(\w):([^;]*);")

# پارامترهای وای‌فای
WIFI_PARAMETERS = {
    "H": "Hidden Network",
    "P": "Password",
    "S": "SSID",
    "T": "Authentication Type",
}


def welcome():
    print("👋 خوش آمدی به برنامه تشخیص رمز وای‌فای با بارکد!")
    print("📷 فقط کافیه تصویر QR رو بدی تا رمز رو برات استخراج کنیم.\n")

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
            save_password_to_file_arguments = {}
            wifi_parameters = WIFI_PARAMETERS_RE.findall(m.group(1))
            for parameter in wifi_parameters:
                if parameter[0] == "P":
                    save_password_to_file_arguments["pw"] = parameter[1]
                elif parameter[0] == "S":
                    save_password_to_file_arguments["ssid"] = parameter[1]
                print(f"{WIFI_PARAMETERS.get(parameter[0]) or parameter[0]}: {parameter[1]}")
            save_password_to_file(**save_password_to_file_arguments)
            return save_password_to_file_arguments.get("pw")
        else:
            print("\nℹ این QR مربوط به وای‌فای نیست یا فرمتش متفاوت است.")
            return None

def save_password_to_file(ssid, pw, filename="wifi_password.txt"):
    """ذخیره SSID و Password در فایل متنی با تاریخ."""
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, mode="w", encoding="utf-8") as f:
            f.write(f"زمان ذخیره‌سازی: {now}\nSSID: {ssid}\nPassword: {pw}\n")
        print(f"\n📁 رمز وای‌فای در فایل '{filename}' ذخیره شد.")
    except Exception as e:
        print("❌ خطا در ذخیره‌سازی رمز:", e)

if __name__ == "__main__":
    welcome()
    args = argparser.parse_args()
    read_qr_offline(args.image_path)
