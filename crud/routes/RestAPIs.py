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
       return {'error': f"Internal server error: {error}"}, 500

# GET /restapis/<id> - Get a REST API by its ID.
def get_restapi_by_id(id):
    try:
        result = repo.get_by_id(id)

        if result is None:
            return {'error': 'Δεν υπάρχει REST API με αυτό το ID.'}, 404

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# POST /restapis - Create a REST API.
def add_restapi():
    try:
        data = request.get_json()
        result = repo.add(data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 201
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# PUT /restapis/<id> - Update a REST API by its ID.
def edit_restapi(id):
    try:
        data = request.get_json()
        result = repo.edit(id, data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# DELETE /restapis/<id> - Delete a REST API by its ID.
def delete_restapi(id):
    try:
        result = repo.delete(id)
                
        if isinstance(result, dict) and "error" in result:
            return result, 400

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500