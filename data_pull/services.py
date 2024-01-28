from data_pull.models import Record
from data_pull.helpers import RequestData, get_predicted_size, get_size
from common.logging_helper import cron_logging as _l

def update_data_from_third_party_api():
    try:
        request_obj = RequestData()
        data = request_obj.get_data()

        for item in data:
            predicted_size, level, real_size, is_win = Record.BIG, 0, Record.BIG, True
            if Record.objects.exists():
                try:
                    query_set = Record.objects.all().order_by("-issue_number")
                    last_obj = query_set[0]
                    second_last_obj = query_set[1]
                except Exception as e:
                    # last_obj = Record.objects.latest("created_at")
                    _l.logger.exception(e)
                    return

                last_level = 0 if not last_obj else last_obj.level
                _, predicted_size = get_predicted_size(last_obj.premium, second_last_obj.premium)
                real_size = get_size(int(item['number']))
                is_win = True
            
                if predicted_size != real_size:
                    is_win = False
                    level = last_level + 1
                else:
                    level = 1

            if not Record.objects.filter(issue_number=item['issueNumber']).exists():
                obj = Record.objects.get_or_create(
                    issue_number=item['issueNumber'],
                    number = item['number'],
                    premium = item['premium'],
                    colour = item['colour'],
                    size_prediction = predicted_size.upper(),
                    level = level,
                    size = real_size,
                    is_win = is_win
                )

                _l.logger.debug("Record added: %s\t",str(obj))
    except Exception as e:
        _l.logger.exception(e)
        raise e
    