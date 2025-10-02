import os
from notion_client import Client
from datetime import datetime
import pytz

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

def get_today_title():
    korea_time = datetime.now(pytz.timezone("Asia/Seoul"))
    return korea_time.strftime("%Y-%m-%d")

def query_page_by_title(title):
    results = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "property": "Name",
                "title": {
                    "equals": title
                }
            }
        }
    ).get("results")

    if results and len(results) > 0:
        return results[0]["id"]
    return None

from datetime import datetime

def create_page_with_title(title):
    new_page = notion.pages.create(
        **{
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": title
                    }
                }
            }
        }
    )
    return new_page["id"]

import time
from notion_client.errors import APIResponseError

def append_file_as_single_block(page_id, filename, retries=3, delay=2):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        return

    for i in range(retries):
        try:
            return notion.blocks.children.append(
                block_id=page_id,
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": content}
                                }
                            ]
                        }
                    }
                ]
            )
        except APIResponseError as e:
            print(f"[Retry {i+1}/{retries}] Failed to append block: {e}")
            time.sleep(delay)

    raise Exception(f"Failed to append block after {retries} retries")

def main():
    today = get_today_title()
    page_id = query_page_by_title(today)
    if not page_id:
        page_id = create_page_with_title(today)
        print(f"Created new page with id: {page_id}")
    else:
        print(f"Found existing page with id: {page_id}")

    append_file_as_single_block(page_id, "output_1.txt")
    append_file_as_single_block(page_id, "output_3.txt")
    print("Appended data to Notion page successfully.")

if __name__ == "__main__":
    main()
