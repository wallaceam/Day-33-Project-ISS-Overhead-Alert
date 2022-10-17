import requests
from datetime import datetime
import smtplib

MY_LAT = 59.329323
MY_LONG = 18.068581
EMAIL = "test@gmail.com"
PASSWORD = "abc123"
iss_nearby = False

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

if (MY_LAT-5) <= iss_latitude <= (MY_LAT+5) and (MY_LONG-5) <= iss_longitude <= (MY_LONG+5):
    iss_nearby = True

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

if iss_nearby and (time_now.hour <= sunrise or time_now.hour >= sunset):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg="Subject: ISS Overhead!\n\nLook up!"
        )
