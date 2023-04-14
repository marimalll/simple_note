import datetime as dt
import requests


def weather_forecast(city):
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
    api_key = '53fb1ef4a169de0c050e695c6e91d199'
    city = city

    params = {"appid": api_key,
              "q": city,
              "lang": 'ru'}


    def kelvin_to_celsius(kelvin):
        celsius = kelvin - 273.15
        return celsius


    response = requests.get(BASE_URL, params=params)
    if response:
        response_json = response.json()
        real_temperature = kelvin_to_celsius(response_json['main']['temp'])
        feels_like_temperature = kelvin_to_celsius(response_json['main']['feels_like'])
        wind_speed = response_json['wind']['speed']
        humidity = response_json['main']['humidity']
        description = response_json['weather'][0]['description']
        icon_url = "https://openweathermap.org/img/wn/" + response_json['weather'][0]['icon'] + "@2x.png"
        pressure = response_json['main']['pressure']
        sunrise_time = dt.datetime.utcfromtimestamp(response_json['sys']['sunrise'] + response_json['timezone']).strftime('%d.%m.%Y %H:%M') # для того чтоб отображать время восхода в локальном времени
        sunset_time = dt.datetime.utcfromtimestamp(response_json['sys']['sunset'] + response_json['timezone']).strftime('%d.%m.%Y %H:%M')
        print(str(icon_url))
        print(type(icon_url))
        return [dt.datetime.now().strftime('%d.%m.%Y %H:%M'),
                f"Температура в {city}: {round(real_temperature, 2)}C", f"Ощущается как: {round(feels_like_temperature, 2)}C",
                f"Скорость ветра: {wind_speed} метров в секунду", f"Влажность: {humidity}", f"{description}", f"Давление: {pressure} мм.рт.ст",
                f"время восхода солнца: {sunrise_time}", f"время заката: {sunset_time}"], icon_url

    else:
        return ['Введите местоположение корректно'], "https://openweathermap.org/img/wn/02d@2x.png"
