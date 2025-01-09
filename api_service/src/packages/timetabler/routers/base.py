from dataclasses import dataclass
from src.packages.timetabler.controllers import Controller
from src.packages.timetabler.services import DatabaseService
from flask import Blueprint, jsonify

@dataclass
class Router():
    router_name:str
    controller:Controller
    service:DatabaseService
    api:Blueprint=None

    def __post_init__(self):
        self._register_routes()
    def _register_routes(self):
        raise NotImplementedError()
    
    def send_response(self,response):
        return jsonify({
        "data":response['data'] if response.get("data") else None,
        "error":response['error'] if response.get("error") else None, 
        "message":response['message'] if response.get("message") else None

        }), response['status_code']
