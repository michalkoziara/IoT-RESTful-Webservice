from flask import json
from flask import Response
from werkzeug.exceptions import HTTPException

import app.main.controller.admin_controller
import app.main.controller.device_group_controller
import app.main.controller.executive_device_controller
import app.main.controller.executive_type_controller
import app.main.controller.formula_controller
import app.main.controller.hub_controller
import app.main.controller.log_controller
import app.main.controller.sensor_controller
import app.main.controller.sensor_type_controller
import app.main.controller.unconfigured_device_controller
import app.main.controller.user_controller
import app.main.controller.user_group_controller
from app import api


@api.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = json.dumps(
            {
                "errorMessage": e.description,
            }
        )
        response.content_type = "application/json"
    else:
        response = Response(
            response=json.dumps(
                {
                    "errorMessage": repr(e),
                }
            ),
            status=500,
            mimetype='application/json'
        )

    return response
