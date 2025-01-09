from dataclasses import dataclass
from flask import jsonify, request, Blueprint

from .base import Router

# DayRouter class that inherits from Router
@dataclass
class DayRouter(Router):
    """
    DayRouter class to handle all Day-related routes.
    This class is responsible for the router logic and calling controller methods.
    """



    def _register_routes(self):
        self.api = Blueprint(self.router_name,__name__)
        """ Register all routes for the day API """
        self.api.add_url_rule('/days', 'create_day', self.create_day, methods=['POST'])
        self.api.add_url_rule('/days/<string:day_id>', 'get_day', self.get_day, methods=['GET'])
        self.api.add_url_rule('/days/<string:day_id>', 'update_day', self.update_day, methods=['PUT'])
        self.api.add_url_rule('/days/<string:day_id>', 'delete_day', self.delete_day, methods=['DELETE'])

    def create_day(self):
        """ Route to create a new day """
        data = request.get_json()
        day_name = data.get('day_name')
        response = self.controller.create_day(day_name)
        return self.send_response(response=response)
    
    def get_day(self, day_id):
        """ Route to get a day by ID """
        response = self.controller.get_day(day_id)
        return self.send_response(response=response)

    def update_day(self, day_id):
        """ Route to update a day by ID """
        data = request.get_json()
        new_day_name = data.get('new_day_name')
        response = self.controller.update_day(day_id, new_day_name)
        return self.send_response(response=response)

    def delete_day(self, day_id):
        """ Route to delete a day by ID """
        response = self.controller.delete_day(day_id)
        return self.send_response(response=response)
