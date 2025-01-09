#!/bin/bash

# Start the Python application
python main.py &

# Start the Celery worker with autoscaling
celery -A main worker --loglevel=INFO --autoscale=10,3