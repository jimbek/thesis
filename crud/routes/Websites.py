# Εδώ δηλώνονται τα routes για τον πίνακα 'Websites'.
from crud.repos.WebsitesRepository import WebsitesRepository

from flask import request

repo = WebsitesRepository()

# GET /websites.
def get_websites():
    try:
        return repo.get_all(), 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# GET /websites/<id>.
def get_website_by_id(id):
    try:
        result = repo.get_by_id(id)

        if result is None:
            return {'error': 'Δεν υπάρχει Website με αυτό το ID.'}, 404

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# POST /websites.
def add_website():
    try:
        data = request.get_json()
        result = repo.add(data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 201
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# PUT /websites/<id>.
def edit_website(id: str):
    try:
        data = request.get_json()
        result = repo.edit(id, data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# DELETE /websites/<id>.
def delete_website(id):
    try:
        result = repo.delete(id)
        
        if isinstance(result, dict) and "error" in result:
            return result, 400

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500