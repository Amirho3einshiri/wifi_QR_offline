# WiFi QR Offline Reader

**WiFi QR Offline Reader** is a simple offline Python tool to read WiFi QR codes from images and extract network credentials (SSID and password) without needing an internet connection.

## Features
- Fully **offline** – works without internet  
- Reads **WiFi QR codes** from images  
- Extracts **SSID** and **password** from QR code  
- Supports common image formats (PNG, JPG, etc.)  

## Installation
Make sure you have **Python 3.8+** installed.  
Install the required dependencies:

```bash
pip install pyzbar pillow

Usage
Edit the IMAGE_PATH variable in wifi_QR_offline.py to point to your QR code image:
IMAGE_PATH = r"C:\path\to\your\qr_code.png"

Then run the script:
python wifi_QR_offline.py

Example Output
QR text detected:
WIFI:S:MyWiFiNetwork;P:MySecurePassword123;

WiFi detected:
SSID: MyWiFiNetwork
Password: MySecurePassword123
If the QR code is not a WiFi QR or the format is different, the program will notify you.
