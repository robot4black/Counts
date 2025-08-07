import requests
import os
import random
from datetime import datetime
import pytz
import time

access_token = os.getenv('ACCESS_TOKEN')
url = os.getenv('URL')
one = os.getenv('ONE')
three = os.getenv('THREE')


korea_timezone = pytz.timezone('Asia/Seoul')

optional_fields = [
    "media_count",
    "username",
    "biography",
    "follows_count",
    "is_published",
    "name"
]

def fetch_and_write_data(username, filename):
    try:
        random_fields = random.sample(optional_fields, random.randint(2, 4))
        all_fields = ",".join(["followers_count"] + random_fields)

        # 构建请求参数
        params = {
            'fields': f'business_discovery.username({username}){{{all_fields}}}',
            'access_token': access_token
        }

        # 请求数据
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get("business_discovery")
            followers_count = data.get('followers_count', "Unknown count")
            time_now = datetime.now(korea_timezone)
            formatted_time = time_now.strftime('%Y-%m-%d %H:%M:%S')

            with open(filename, 'a') as file:
                file.write(f"{username},{followers_count},{formatted_time}\n")

            print(f"{username},{followers_count},{formatted_time}")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Failed: {e}")


for i in range(12):
    try:
        fetch_and_write_data(one, 'output_1.txt')
        fetch_and_write_data(three, 'output_3.txt')
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Data written successfully. Run {i+1}/12")
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error occurred: {e}")
    sleep_seconds = random.randint(240, 360)
    time.sleep(sleep_seconds)
