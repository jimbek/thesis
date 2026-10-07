# Defines the routes for the 'RestAPIs' table.
from crud.repos.RestAPIsRepository import RestAPIsRepository

from flask import request

# Initialize the RestAPIsRepository.
repo = RestAPIsRepository()

# GET /restapis - Get all REST APIs.
def get_restapis():
    try:
        return repo.get_all(), 200
    except Exception as error:
        return f"Internal server error: {error}", 500

# POST /restapis - Create a REST API.
def create_restapi():
    try:
        data = request.get_json()

        if data is None:
            return "Body is missing", 400
        
        if not data.get("name") or not data.get("description") or not data.get("domain") or not data.get("openapi_spec"):
            return "Invalid parameters", 400
        
        return repo.add(data), 201
    except Exception as error:
        return f"Internal server error: {error}", 500