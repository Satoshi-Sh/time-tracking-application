import requests
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_token = os.getenv("API_TOKEN")
app_id = os.getenv("APP_ID")
domain_name = os.getenv("DOMAIN_NAME")
url = f"https://{domain_name}.kintone.com/k/v1/records.json"


headers = {"X-Cybozu-API-Token": api_token}


def get_todays_data():
    params = {"app": app_id, "query": "date = TODAY()"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        records = response.json()["records"]
        df = pd.DataFrame()
        for record in records:
            username = record.get("username", {}).get("value", "")
            time = record.get("time", {}).get("value", "")
            task = record.get("task", {}).get("value", "")
            date = record.get("date", {}).get("value", "")
            status = record.get("status", {}).get("value", "")
            time_amount = record.get("time_amount", {}).get("value", "")

            df = df._append(
                {
                    "Username": username,
                    "Time": time,
                    "Task": task,
                    "Date": date,
                    "Status": status,
                    "Time Amount": time_amount,
                },
                ignore_index=True,
            )
        return df
    else:
        print(f"Error: {response.status_code} - {response.text}")


def post_record(data):
    params = {"app": app_id, "records": [data]}
    resp = requests.post(url, json=params, headers=headers)
    return resp


# sample_record = {
#     "username": {"value": "JohnDoe"},
#     "time": {"value": "16:00"},
#     "task": {"value": "Complete Project X"},
#     "date": {"value": "2022-01-13"},
#     "status": {"value": "Break"},
#     "time_amount": {"value": 100},
# }
