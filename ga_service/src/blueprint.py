from flask import Blueprint, request
from .tasks import add_numbers
from celery.result import AsyncResult

bp = Blueprint("operations",__name__)

@bp.post("/add")
def start_add():
    try:
        a = int(request.args.get("a"))
        b = int(request.args.get("b"))
    except (ValueError, TypeError):
        return {"error": "Invalid input. Both 'a' and 'b' must be integers."}, 400

    result = add_numbers.delay(a, b)
    return {"result_id": result.id}

@bp.get("/result/<id>")
def task_result(id: str):
    result = AsyncResult(id)
    response = {
        "state": result.state,  # e.g., PENDING, STARTED, PROGRESS, SUCCESS
        "ready": result.ready(),
        "successful": result.successful(),
    }

    if result.state == "PROGRESS":
        # Include progress if available
        response["progress"] = result.info.get("progress", 0)
    elif result.ready():
        if result.successful():
            response["value"] = result.result
        else:
            response["error"] = str(result.info)  # Exception info or task error

    return response