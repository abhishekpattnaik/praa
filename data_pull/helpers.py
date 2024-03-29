import json
import requests
from datetime import datetime

from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from common.logging_helper import cron_logging as _l
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
        try:
            response = requests.request("POST", self.url, headers=self.headers, data=self.payload)
            if response.status_code == 200:
                d = json.loads(response.text)
                return d["data"]["list"]
            raise
        except Exception as e:
            _l.logger.exception(e)
            _l.logger.error("Failed to fetch data from the API. Status code: %s",response.status_code)
            return []

def list_latest_records() -> QuerySet[Record]:
    return Record.objects.filter(level__gt = 0).order_by('-issue_number')

def get_size(number) -> str:
    return Record.BIG if number > 4 else Record.SMALL

def get_position(issue_number:int) -> int:
    if issue_number == 0: return 8
    elif issue_number == 1: return 7
    elif issue_number == 2: return 6
    elif issue_number == 3: return 5
    elif issue_number == 4: return 2
    elif issue_number == 5: return 4
    elif issue_number == 6: return 9
    elif issue_number == 7: return 10
    elif issue_number == 8: return 3
    elif issue_number == 9: return 1
    # return -1
    
def predict_next_record(last_premium: int, second_last_premium: int, next_issue_number: int) -> (int, str, str):

    ############################ Formula No.1 ################################
    # if last_premium == 0 and :
    #     pass
    # if premium == 0: premium = Record.objects.latest("created_at").premium
    # hashed_value = abs(sum([int(i) for i in str(int(premium / 10))])) % 10


    ############################ Formula No.2 ################################
    if (last_premium % second_last_premium) == 0:
        predicted_number = int(str(last_premium)[-1])
    else:
        predicted_number = int(str(last_premium / second_last_premium).split(".")[1][:get_position(next_issue_number % 10)][-1])

    predicted_size = get_size(predicted_number)

    if predicted_number == 0:
        predicted_color = Record.COLOR_0
    elif predicted_number == 5:
        predicted_color = Record.COLOR_5
    elif (predicted_number % 2) == 0:
        predicted_color = Record.COLOR_EVEN
    else:
        predicted_color = Record.COLOR_ODD

    _l.logger.info("[Prediction] Next Issue Number: %s, Next Predicted Number: %s, Next Predicted Size: %s, Next Predicted Colour: %s", next_issue_number, predicted_number, predicted_size, predicted_color)
    return predicted_number, predicted_size, predicted_color

def fetch_new_records(request) -> dict:
    records_queryset = list_latest_records()
    if records_queryset.count() < 7:
        return {}
    items_per_page = 60
    records = [model_to_dict(obj) for obj in records_queryset]
    total_record = records_queryset.count()
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
    next_number_prediction, next_size_prediction, next_colour_prediction = predict_next_record(records_queryset[4].premium, 
                                                                                               records_queryset[5].premium, 
                                                                                               records_queryset[0].issue_number + 1)
    
    template_data = dict(
            records = your_page,
            your_page = your_page,
            
            win_percentage = round((total_wins/total_record) * 100),
            loss_percentage = round(((total_record - total_wins)/total_record) * 100),
            total_records = total_record,
            total_wins = total_wins,
            total_losses = total_record - total_wins,

            next_issue_number = records_queryset[0].issue_number + 1,
            next_number_prediction = next_number_prediction,
            next_size_prediction = next_size_prediction.upper(),
            next_colour_prediction = Record.COLOR_EVEN if Record.COLOR_EVEN in next_colour_prediction else Record.COLOR_ODD,

            reload_after_delta = 62 - datetime.now().second
        )
    return template_data
