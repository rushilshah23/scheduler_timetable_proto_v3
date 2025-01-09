import os
from src.app import create_app

flask_app = create_app()
celery_app = flask_app.extensions['CELERY_APP']


if __name__ == "__main__":
    flask_app.run(host=os.environ.get("HOST"), port=os.environ.get("PORT"),debug=True)

