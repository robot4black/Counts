import time
from concurrent.futures import ThreadPoolExecutor
import requests
from datetime import datetime
import pytz
import os

korea_timezone = pytz.timezone('Asia/Seoul')
one = os.getenv('ONE')
three = os.getenv('THREE')

filename_map = {
    one: "output_1.txt",
    three: "output_3.txt"
}

def fetch_user_data(username):
    base_url = os.getenv("API_BASE_URL")
    referer = os.getenv("REFERER")
    origin = os.getenv("ORIGIN")
    url = f"{base_url}{username}"
    headers = {
        "Referer": referer,
        "Origin": origin,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data.get("success"):
            username = data["user"]["username"]
            followers = data["user"]["followerCount"]
            return {"username": username, "followers": followers}
    except Exception as e:
        print("Request failed:", e)

    return None

def write_user_data_to_txt_line(user_data):
    time_now = datetime.now(korea_timezone)
    formatted_time = time_now.strftime('%Y-%m-%d %H:%M:%S')
    filename = filename_map.get(user_data['username'], "output_default.txt")
    with open(filename, "a", encoding="utf-8") as f:
        line = f"{user_data['username']},{user_data['followers']},{formatted_time}\n"
        f.write(line)
        print(f"{filename}: {line.strip()}")

def loop_fetch(usernames, interval, times):
    with ThreadPoolExecutor(max_workers=len(usernames)) as executor:
        for _ in range(times):
            futures = [executor.submit(fetch_user_data, username) for username in usernames]
            for future in futures:
                user_data = future.result()
                if user_data:
                    write_user_data_to_txt_line(user_data)
                else:
                    print("Failed!")
            time.sleep(interval)

if __name__ == "__main__":
    usernames = [one, three]
    loop_fetch(usernames, interval=120, times=15)
