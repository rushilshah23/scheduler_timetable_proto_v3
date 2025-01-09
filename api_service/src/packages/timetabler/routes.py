from flask import Flask, jsonify, request, abort, Blueprint
from sqlalchemy.orm import Session
from . import service, models, schemas
from src.utils import database


from src.packages.timetabler.modules.ga_scale import generate_timetable

from src.packages.timetabler.business.business_utils import Utils
from src.packages.timetabler.business.utils import save_output_file
from src.packages.timetabler.service import CRUDUtilities

timetable_router = Blueprint('timetable_router',__name__)


# Route to create a new day
@timetable_router.route("/days/", methods=["POST"])
def create_day():
    # db: Session = database.SessionLocal()
    db: Session = next(database.get_db())

    service = CRUDUtilities(db_session=db)

    try:
        # Validate the request data
        data = request.get_json()
        if not data or not all(key in data for key in ('id', 'day_name')):
            return jsonify({"error": "Invalid input"}), 400

        # Use the service function to create the day
        created_day = service.create_day(day_data=data)
        if created_day.rowcount == 1:
            return jsonify({
                "message": "Day created successfully",
                "data": {
                    "id": data["id"],
                    "day_name": data["day_name"]
                }
            }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Route to get a day by ID
@timetable_router.route("/days/<string:day_id>", methods=["GET"])
def get_day_by_id(day_id):
    db = next(database.get_db())  # Get the DB session
    service = CRUDUtilities(db_session=db)

    try:
        db_day = service.get_day(day_id=day_id)
        if db_day is None:
            abort(404, description="Day not found")
        return jsonify(db_day.to_dict())
    finally:
        db.close()


# @timetable_router.route("/", methods=['POST'])
# def generate_university_timetable():


#     req_data = request.get_json()

#     # fittest_chromosome = timetable_generator.perform_ga()
    
#     fittest_chromosome = generate_timetable(req_data)

#     # print(fittest_chromosome)
#     university_timetables = fittest_chromosome
#     university_timetables = Utils.sort_slots(fittest_chromosome.genes)


#     print("Saving university timetable ...")
#     # print(university_timetables)
#     save_output_file('output_utt_1.json', university_timetables)
#     from .pdf_service.service_2 import create_class_timetable_pdfs

#     create_class_timetable_pdfs(university_timetables)
#     return {"message":"University timetable created successfully !"}


from src.packages.timetabler.bg_tasks import generate_university_timetable_task
@timetable_router.route("/", methods=['POST'])
def generate_university_timetable():
    req_data = request.get_json()
    # zip_file_path = generate_university_timetable_task(req_data)
    # return send_file(zip_file_path, as_attachment=True)
    # return res


    # task = generate_university_timetable_task.apply_async(args=[req_data], queue='celery')
    task = generate_university_timetable_task.delay(req_data)

    return {"message": "Timetable generation started!", "task_id": task.id}


from flask import jsonify, send_file
from celery.result import AsyncResult
import os

@timetable_router.route("/status/<task_id>", methods=['GET'])
def get_task_status(task_id):
    task = AsyncResult(task_id)

    if task.state == 'PENDING':
        # Task is still processing
        return jsonify({"status": "Processing", "task_id": task.id})
    elif task.state == 'SUCCESS':
        # Task is complete, and result is the path to the zip file
        zip_file_path = task.result

        # Assuming task.result is a relative path, construct the absolute path
        full_path = os.path.join("/usr/src/app", zip_file_path)

        # Check if the file exists before serving
        if os.path.exists(full_path):
            print(f"Serving from -- {full_path}")
            return send_file(full_path, as_attachment=True)
        else:
            return jsonify({"status": "Error", "message": "File not found", "task_id": task.id}), 404

    elif task.state == 'FAILURE':
        # Task failed
        return jsonify({"status": "Failed", "task_id": task.id, "error": str(task.info)})

    else:
        return jsonify({"status": "Unknown", "task_id": task.id})
