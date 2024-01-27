import logging as _l

class Logging:
    def __init__(self, *args, **kwargs) -> None:
        self.logger = _l.getLogger(kwargs.get("logging_name", "common-mysite-prototype"))


common_logging = Logging("common-mysite-prototype")
api_logging = Logging("api-mysite-prototype")
cron_logging = Logging("cron-mysite-prototype")
