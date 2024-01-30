from data_pull.models import Record
from data_pull.helpers import RequestData, predict_next_record, get_size
from common.logging_helper import cron_logging as _l

def update_data_from_third_party_api():
    try:
        request_obj = RequestData()
        data = request_obj.get_data()
        for item in data:
            predicted_size, level, real_size, is_win = Record.BIG, 0, Record.BIG, True
            if Record.objects.count() > 7:
                query_set = Record.objects.all().order_by("-issue_number")

                last_level = 0 if not query_set[0] else query_set[0].level
                predicted_number, predicted_size, predicted_colour = predict_next_record(query_set[4].premium, query_set[5].premium, query_set[0].issue_number + 1)
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
                    premium = item['premium'],
                    level = level,
                    is_win = is_win,

                    # original data update
                    number = item['number'],
                    colour =  Record.COLOR_EVEN if Record.COLOR_EVEN.lower() in item['colour'] else Record.COLOR_ODD,
                    size = Record.BIG if Record.BIG == real_size.upper() else Record.SMALL,

                    # predicted data update
                    predicted_number = predicted_number,
                    predicted_colour = Record.COLOR_EVEN if Record.COLOR_EVEN in predicted_colour else Record.COLOR_ODD,
                    predicted_size = predicted_size.upper()
                )

                _l.logger.debug("Record added: %s\t",str(obj))
    except Exception as e:
        _l.logger.exception(e)
        raise e
    