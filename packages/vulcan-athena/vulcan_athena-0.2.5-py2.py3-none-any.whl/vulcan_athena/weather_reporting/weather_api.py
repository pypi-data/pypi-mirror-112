import numpy as np
import pandas as pd
import json
import datetime as dt
import time
from dateutil import tz

import requests

from vulcan_athena.weather_reporting.setup import (
    api_key,
    melbourne_id,
    geelong_id,
    base_url,
    forecast_url,
    melbourne_lat,
    melbourne_lon,
    geelong_lat,
    geelong_lon,
    exclude_list,
)


def time_converter(unix_time):
    """
    Function to convert unix time to AEST/AEDT
    """
    from_zone = tz.gettz("UTC")
    to_zone = tz.gettz("Australia/Melbourne")

    return (
        dt.datetime.utcfromtimestamp(unix_time)
        .replace(tzinfo=from_zone)
        .astimezone(to_zone)
        .strftime("%Y-%m-%d %H:%M:%S")
    )


def api_parsers(json_data):
    """
    Function to parse the current weather data from the API to python dictionary
    """
    local_time = time_converter(json_data["dt"])
    weather_dict = {
        "name": json_data["name"],
        "lat": json_data["coord"]["lat"],
        "lon": json_data["coord"]["lon"],
        "date": local_time.split()[0],
        "time": local_time.split()[1],
        "weather_main": json_data["weather"][0]["main"],
        "weather_condition": json_data["weather"][0]["description"],
    }
    weather_dict.update(json_data["main"])
    weather_dict["visibility (m)"] = json_data["visibility"]
    weather_dict["clouds %"] = json_data["clouds"]["all"]
    weather_dict["wind_speed (m/s)"] = json_data["wind"]["speed"]

    return weather_dict


def df_generation(json_data):
    df = pd.DataFrame(api_parsers(json_data), index=[0])
    col_names = list(df.columns)

    col_names[7] = col_names[7] + "(C)"
    col_names[8] = col_names[8] + "(C)"
    col_names[9] = col_names[9] + "(C)"
    col_names[10] = col_names[10] + "(C)"
    col_names[11] = col_names[11] + " hPa"
    col_names[12] = col_names[12] + " %"

    df.columns = col_names

    return df


def forecast_api_parser(forecast_unit, city_name="Melbourne"):
    """
    Function to parse the forecast weather data from the API to python dictionary
    """
    forecast_dict = {
        "name": city_name,
        "date": time_converter(forecast_unit["dt"]).split()[0],
        "time": time_converter(forecast_unit["dt"]).split()[1],
        "weather_main": forecast_unit["weather"][0]["main"],
        "weather_condition": forecast_unit["weather"][0]["description"],
        "temp_morn(C)": forecast_unit["temp"]["morn"],
        "feels_like_morn(C)": forecast_unit["feels_like"]["morn"],
        "temp_day(C)": forecast_unit["temp"]["day"],
        "feels_like_day(C)": forecast_unit["feels_like"]["day"],
        "temp_eve(C)": forecast_unit["temp"]["eve"],
        "feels_like_eve(C)": forecast_unit["feels_like"]["eve"],
        "temp_night(C)": forecast_unit["temp"]["night"],
        "feels_like_night(C)": forecast_unit["feels_like"]["night"],
        "temp_min(C)": forecast_unit["temp"]["min"],
        "temp_max(C)": forecast_unit["temp"]["max"],
        "pressure hPa": forecast_unit["pressure"],
        "humidity %": forecast_unit["humidity"],
        "wind_speed (m/s)": forecast_unit["wind_speed"],
        "cloudiness %": forecast_unit["clouds"],
        "uv_max_index %": forecast_unit["uvi"],
        "rain mm": forecast_unit["rain"] if "rain" in forecast_unit.keys() else 0,
        "rain_probability %": forecast_unit["pop"],
    }

    return pd.DataFrame(forecast_dict, index=[0])


# current weather wrapper function
def call_current_weather(api_key=api_key):
    """
    Function that calls the current weather API using the OpenWeather app

    :param api_key: user API key
    :type api_key: str
    :return: Melbourne & Geelong current weather data
    :rtype: dataframe
    """
    # getting weather information on Melbourne
    api_address_melb = (
        base_url + "appid=" + api_key + "&id=" + melbourne_id + "&units=metric"
    )
    json_data_melb = requests.get(api_address_melb).json()

    df_melb = df_generation(json_data_melb)

    # getting weather information on Geelong
    api_address_geelong = (
        base_url + "appid=" + api_key + "&id=" + geelong_id + "&units=metric"
    )
    json_data_geelong = requests.get(api_address_geelong).json()

    df_geelong = df_generation(json_data_geelong)

    # return both the weather information together
    return df_melb.append(df_geelong)


def forecast_weather(
    forecast_url, lat, lon, exclude_list, api_key, city_name="Melbourne"
):
    """
    Function that loops each forecast day to pass through the forecast parser
    """
    forecast_address = (
        forecast_url
        + "lat="
        + lat
        + "&lon="
        + lon
        + "&exclude="
        + exclude_list
        + "&appid="
        + api_key
        + "&units=metric"
    )
    forecast_data = requests.get(forecast_address).json()

    forecast_list = []
    for f_cast in forecast_data["daily"]:
        forecast_list.append(forecast_api_parser(f_cast, city_name))

    return pd.concat(forecast_list, ignore_index=True)


# forecast weather wrapper function
def call_forecast_weather(api_key=api_key):
    """
    Function that calls the forecast weather One Call API using the OpenWeather app
    :param api_key: user API key
    :type api_key: str
    :return: 7 days forecast weather for Melbourne & Geelong
    :rtype: dataframe
    """
    df_forecast_melbourne = forecast_weather(
        forecast_url, melbourne_lat, melbourne_lon, exclude_list, api_key, "Melbourne"
    )
    df_forecast_geelong = forecast_weather(
        forecast_url, geelong_lat, geelong_lon, exclude_list, api_key, "Geelong"
    )

    return df_forecast_melbourne.append(df_forecast_geelong)
