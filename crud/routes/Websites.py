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

# POST /websites - Create a website.
def add_website():
    try:
        data = request.get_json()

        if data is None:
            return "Body is missing", 400
        
        if not data.get("name") or not data.get("description") or not data.get("domain"):
            return "Invalid parameters", 400
        
        return repo.add(data), 201
    except Exception as error:
        return f"Internal server error: {error}", 500

# PUT /websites/<id> - Update a website by its ID.
def edit_website(id):
    try:
        data = request.get_json()

        if data is None:
            return "Body is missing", 400
        
        return repo.edit(id, data), 200
    except Exception as error:
        return f"Internal server error: {error}", 500

# DELETE /websites/<id> - Delete a website by its ID.
def delete_website(id):
    try:
        return repo.delete(id), 200
    except Exception as error:
        return f"Internal server error: {error}", 500   