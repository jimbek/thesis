# Εδώ δηλώνονται τα routes για τον πίνακα 'RestAPIs'.
from crud.repos.RestAPIsRepository import RestAPIsRepository

from flask import request

repo = RestAPIsRepository()

# GET /restapis.
def get_restapis():
    try:
        return repo.get_all(), 200
    except Exception as error:
       return {'error': f"Internal server error: {error}"}, 500

# GET /restapis/<id>.
def get_restapi_by_id(id):
    try:
        result = repo.get_by_id(id)

        if result is None:
            return {'error': 'Δεν υπάρχει REST API με αυτό το ID.'}, 404

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# POST /restapis.
def add_restapi():
    try:
        data = request.get_json()
        result = repo.add(data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 201
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# PUT /restapis/<id>.
def edit_restapi(id):
    try:
        data = request.get_json()
        result = repo.edit(id, data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# DELETE /restapis/<id>.
def delete_restapi(id):
    try:
        result = repo.delete(id)
                
        if isinstance(result, dict) and "error" in result:
            return result, 400

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500