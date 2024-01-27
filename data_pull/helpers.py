import json
import requests
from datetime import datetime

from django.forms.models import model_to_dict
from django.core.paginator import Paginator

from data_pull.models import Record

class RequestData:
    def __init__(self, **kwargs) -> None:
        self.url = kwargs.get("url", "https://api.damanplatform.com/api/webapi/GetNoaverageEmerdList")
        self.payload = kwargs.get("payload","{\"pageSize\":10,\"pageNo\":1,\"typeId\":1,\"language\":0,\"random\":\"db695f3f5f5642a894dc8117546c51f7\",\"signature\":\"BE4AF840C43F958124FBAC9012BA5AAD\",\"timestamp\":1706256121}")
        self.headers = kwargs.get(
            "headers", {
                # 'authority': 'api.damanplatform.com',
                # 'accept': 'application/json, text/plain, */*',
                # 'accept-language': 'en-GB,en;q=0.9',
                # 'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIxNzA2MjU1NTkyIiwibmJmIjoiMTcwNjI1NTU5MiIsImV4cCI6IjE3MDYyNTczOTIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIxLzI2LzIwMjQgMTo1MzoxMiBQTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkFjY2Vzc19Ub2tlbiIsIlVzZXJJZCI6IjQ3NTQ2ODEiLCJVc2VyTmFtZSI6IjkxNzAwODI1MDUwMiIsIlVzZXJQaG90byI6IjIwIiwiTmlja05hbWUiOiJNZW1iZXJOTkdNREJFWSIsIkFtb3VudCI6IjYuMDgiLCJJbnRlZ3JhbCI6IjAiLCJMb2dpbk1hcmsiOiJINSIsIkxvZ2luVGltZSI6IjEvMjYvMjAyNCAxOjIzOjEyIFBNIiwiTG9naW5JUEFkZHJlc3MiOiI0NS4xMjEuMi41MyIsIkRiTnVtYmVyIjoiMCIsIklzdmFsaWRhdG9yIjoiMCIsIktleUNvZGUiOiI2MjgiLCJUb2tlblR5cGUiOiJBY2Nlc3NfVG9rZW4iLCJQaG9uZVR5cGUiOiIwIiwiVXNlclR5cGUiOiIwIiwiVXNlck5hbWUyIjoiIiwiaXNzIjoiand0SXNzdWVyIiwiYXVkIjoibG90dGVyeVRpY2tldCJ9.0MRjxOGZFUS0Azg7JCZNrZDZNfACl9sebX7vqIqn9NM',
                'content-type': 'application/json;charset=UTF-8',
                # 'origin': 'https://damanclub.net',
                # 'referer': 'https://damanclub.net/',
                # 'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                # 'sec-ch-ua-mobile': '?0',
                # 'sec-ch-ua-platform': '"macOS"',
                # 'sec-fetch-dest': 'empty',
                # 'sec-fetch-mode': 'cors',
                # 'sec-fetch-site': 'cross-site',
                # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            )

    def get_data(self) -> list:
        response = requests.request("POST", self.url, headers=self.headers, data=self.payload)
        d = json.loads(response.text)
        if response.status_code == 200:
            return d["data"]["list"]

        print(f"Failed to fetch data from the API. Status code: {response.status_code}")
        return []

def get_size(number) -> str:
    return Record.BIG if number > 4 else Record.SMALL

def get_predicted_size(premium: int = 0) -> str:
    if premium == 0: premium = Record.objects.latest("created_at").premium
    hashed_value = abs(sum([int(i) for i in str(int(premium / 10))])) % 10
    return get_size(hashed_value)

def fetch_new_records(request) -> dict:

    last_object = Record.objects.latest("issue_number")
    items_per_page = 60
    records = [model_to_dict(obj) for obj in Record.objects.filter(level__gt = 0).order_by('-issue_number')]
    total_record = len(records)
    total_wins = 0
    for i in records:
        if i["is_win"]:
            total_wins += 1
            i["result"] = "WIN"
        else:
            i["result"] = "LOSS"

    paginator = Paginator(records, items_per_page)
    page = request.GET.get('page', 1)
    your_page = paginator.get_page(page)
    reloading_time = 62 - datetime.now().second
    
    template_data = dict(
            records = your_page,
            your_page = your_page,
            win_percentage = round((total_wins/total_record) * 100),
            loss_percentage = round(((total_record - total_wins)/total_record) * 100),
            total_records = total_record,
            total_wins = total_wins,
            total_losses = total_record - total_wins,
            next_prediction = get_predicted_size(last_object.premium).upper(),
            next_issue_number = last_object.issue_number + 1,
            reload_after_delta = reloading_time
        )
    return template_data
