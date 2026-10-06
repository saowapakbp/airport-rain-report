import argparse
import json
import os
from datetime import datetime, timedelta, timezone

import requests

LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"
BANGKOK = timezone(timedelta(hours=7))
RAW_BASE = "https://raw.githubusercontent.com/{repo}/main/reports"


def push(messages):
    headers = {"Authorization": f"Bearer {os.environ['LINE_CHANNEL_ACCESS_TOKEN']}", "Content-Type": "application/json"}
    payload = {"to": os.environ["LINE_USER_ID"], "messages": messages}
    response = requests.post(LINE_PUSH_URL, headers=headers, data=json.dumps(payload), timeout=15)
    print("push status:", response.status_code, response.text)
    response.raise_for_status()


def report_messages(local_date, repo):
    base = RAW_BASE.format(repo=repo)
    text = f"รายงานพยากรณ์ฝนสะสม 24 ชม. รายท่าอากาศยาน\nวันที่ {local_date} (07:00–07:00 น.)\nตรวจแล้วส่งต่อกลุ่มกองฯ"
    image = {"type": "image",
             "originalContentUrl": f"{base}/report_{local_date}.png",
             "previewImageUrl": f"{base}/report_{local_date}_preview.jpg"}
    return [{"type": "text", "text": text}, image]


def failure_messages(local_date, run_url):
    text = f"สร้างรายงานฝนสะสมวันที่ {local_date} ไม่สำเร็จ\nดูรายละเอียด: {run_url}"
    return [{"type": "text", "text": text}]


def main():
    parser = argparse.ArgumentParser(description="Push the daily rainfall report image to LINE")
    parser.add_argument("--date", default=datetime.now(BANGKOK).strftime("%Y-%m-%d"))
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "saowapakbp/airport-rain-report"))
    parser.add_argument("--failed", action="store_true", help="send a failure notice instead of the report")
    parser.add_argument("--run-url", default="")
    args = parser.parse_args()
    messages = failure_messages(args.date, args.run_url) if args.failed else report_messages(args.date, args.repo)
    push(messages)


if __name__ == "__main__":
    main()
