# Defines the routes for the 'Websites' table.
from crud.repos.WebsitesRepository import WebsitesRepository

from flask import request

# Initialize the WebsitesRepository.
repo = WebsitesRepository()

# GET /websites - Get all websites.
def get_websites():
    try:
        return repo.get_all(), 200
    except Exception as error:
        return f"Internal server error: {error}", 500

# GET /websites/<id> - Get a website by its ID.
def get_website_by_id(id):
    try:
        result = repo.get_by_id(id)

        if result is None:
            return {'error': 'Δεν υπάρχει Website με αυτό το ID.'}, 404

        return result, 200
    except Exception as error:
        return f"Internal server error: {error}", 500

# POST /websites - Create a website.
def add_website():
    try:
        data = request.get_json()
        result = repo.add(data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 201
    except Exception as error:
        return f"Internal server error: {error}", 500

# PUT /websites/<id> - Update a website by its ID.
def edit_website(id: str):
    try:
        data = request.get_json()
        result = repo.edit(id, data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# DELETE /websites/<id> - Delete a website by its ID.
def delete_website(id):
    try:
        result = repo.delete(id)
        
        if isinstance(result, dict) and "error" in result:
            return result, 400

        return result, 200
    except Exception as error:
        return f"Internal server error: {error}", 500   