import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
LATITUDE = float(os.getenv('LATITUDE'))
LONGITUDE = float(os.getenv('LONGITUDE'))
TIMEZONE = os.getenv('TIMEZONE')

def send_email(subject, body):
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, EMAIL_PASSWORD)
    text = message.as_string()
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
    server.quit()

def get_first_kp_index(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    spans = soup.find_all('span', class_='HideInfo1')
    for span in spans:
        lines = span.get_text().split('\n')
        for line in lines:
            if "the Geomagnetic Activity level (Kp number) will be" in line:
                parts = line.split()
                try:
                    kp_index_position = parts.index("be") + 1
                    kp_index = float(parts[kp_index_position])
                    if kp_index >= 2.0: # Trigger notification for Kp values of # or higher
                        return kp_index
                except (IndexError, ValueError):
                    continue
    return None

def get_sun_times(lat, lon, date='today', tz=TIMEZONE):
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date}&formatted=0"
    response = requests.get(url)
    data = response.json()['results']
    sunrise = datetime.fromisoformat(data['sunrise']).astimezone(pytz.timezone(tz))
    sunset = datetime.fromisoformat(data['sunset']).astimezone(pytz.timezone(tz))
    return sunrise, sunset

def is_within_notification_period(lat, lon):
    now = datetime.now(pytz.timezone(TIMEZONE))
    sunrise, sunset = get_sun_times(lat, lon, tz=TIMEZONE)
    after_sunset = sunset + timedelta(hours=1.5)
    before_sunrise = sunrise - timedelta(hours=1.5)
    return now >= after_sunset or now <= before_sunrise

if __name__ == '__main__':
    url = 'https://softservenews.com/'
    while True:
        if is_within_notification_period(LATITUDE, LONGITUDE):
            kp_value = get_first_kp_index(url)
            if kp_value is not None:
                print(f"Kp value: {kp_value}")
                send_email(f"AURORA ALERT: {kp_value} Kp", f".")
            else:
                print("No significant Kp value found.")
        else:
            print("Outside notification period.")
        time.sleep(1600)