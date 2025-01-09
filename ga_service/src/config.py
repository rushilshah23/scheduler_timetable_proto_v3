import os
from dotenv import load_dotenv

load_dotenv()

class CeleryConfig(object):
    broker_url = os.environ.get("CELERY_BROKER_URL")
    result_backend = os.environ.get("CELERY_RESULT_BACKEND")
    task_ignore_result = True


class AppConfig(object):
    CELERY_CONFIG = CeleryConfig
