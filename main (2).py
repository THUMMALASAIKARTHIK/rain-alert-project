import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "AC854f4ac5decef63d00ad83601e18a12e"
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    "lat": 12.916336934870985,
    "lon": 77.61561899533031,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
will_rain=False
for hour_data in weather_data["list"]:
  condition_code=hour_data["weather"][0]["id"]
  if int(condition_code)<700:
     will_rain=True
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client=Client(account_sid,auth_token,http_client=proxy_client)
    message=client.messages.create(
    body="its going to rain today.remember to bring an umbrella ☔.",
    from_='+17066087488',
    to='+917032598604'
    )
    print(message.status)