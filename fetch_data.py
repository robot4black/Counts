import requests
import os
import json
from datetime import datetime
import pytz
import time

access_token = os.getenv('ACCESS_TOKEN')
url = os.getenv('URL')
one = os.getenv('ONE')
three = os.getenv('THREE')

params1 = {
    'fields': f'business_discovery.username({one}){{followers_count,username}}',
    'access_token': access_token
}
params2 = {
    'fields': f'business_discovery.username({three}){{followers_count,username}}',
    'access_token': access_token
}

korea_timezone = pytz.timezone('Asia/Seoul')

def fetch_and_write_data(params, filename):
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get("business_discovery")
            username = data.get('username', "Unknown user")
            followers_count = data.get('followers_count', "Unknown count")
            time_now = datetime.now(korea_timezone)
            formatted_time = time_now.strftime('%Y-%m-%d %H:%M:%S')
            with open(filename, 'a') as file:
                file.write(f"{username},{followers_count},{formatted_time}\n")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Failed: {e}")


try:
    fetch_and_write_data(params1, 'output_1.txt')
    fetch_and_write_data(params2, 'output_3.txt')
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Data written successfully.")
except Exception as e:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error occurred: {e}")
time.sleep(120)
