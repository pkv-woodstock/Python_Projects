import requests
import os
from email.message import EmailMessage
import smtplib

api_key = os.environ.get("OWM_API")
print(api_key)
# api_key = "a35bc1d890601564f06b2a67442e8379"
OWM_Endpoint = 'https://api.openweathermap.org/data/2.5/weather'

weather_params = {
    'appid': api_key,
    'q': 'Bengaluru,India',
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
# print(response.status_code)
weather_data = response.json()
print(weather_data)
# print(weather_data["weather"][0]["id"])
# print(weather_data["weather"][0]["description"])
weather_description = weather_data["weather"][0]["description"]

email = EmailMessage()
email['from'] = 'Pavan Kumar V'
email['to'] = 'rvit21bcs044.rvitm@rvei.edu.in'
email['subject'] = "Today's weather"

email.set_content(weather_description)

with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login('pavankumarvpkv@gmail.com', 'dooy hoqv albr ogen')
    smtp.send_message(email)
    print('all good boss!')
