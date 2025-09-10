import requests
import logging
import pandas as pd
import os

WEATHER_DATA_API_HOST = os.environ.get("WEATHER_DATA_API_HOST", "")

logger = logging.getLogger(__name__)


post_url = WEATHER_DATA_API_HOST


def get_data(latitude=52.5200, longitude=13.4050):
    session = requests.Session()

    # TODO one shouldn't need a csrftoken for server to server
    # fetch CSRF token
    csrf_response = session.get(WEATHER_DATA_API_HOST + "get_csrf_token/")
    csrftoken = csrf_response.json()["csrfToken"]

    payload = {"latitude": latitude, "longitude": longitude}

    headers = {
        "X-CSRFToken": csrftoken,
        "Referer": post_url,
    }

    post_response = session.post(post_url, data=payload, headers=headers)
    # TODO here would be best to return a token but this requires celery on the weather_data API side
    # If we get a high request amount we might need to do so anyway
    if post_response.status_code == 200:
        df = pd.DataFrame(post_response.json()["variables"])
        logger.info("The weather data API fetch worked successfully")
    else:
        df = pd.DataFrame()
        logger.error("The weather data API fetch did not work")
    return df

if __name__=="__main__":
    print(get_data())