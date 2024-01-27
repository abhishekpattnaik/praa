import logging as _l

class Logging:
    def __init__(self, *args, **kwargs) -> None:
        self.logger = _l.getLogger(kwargs.get("logging_name", "common-mysite-prototype"))


common_logging = Logging(logging_name = "common-mysite-prototype")
api_logging = Logging(logging_name = "api-mysite-prototype")
cron_logging = Logging(logging_name = "cron-mysite-prototype")
