# Defines the routes for the 'LLMs' table.
from crud.repos.LLMsRepository import LLMsRepository

from flask import request

# Initialize the LLMsRepository.
repo = LLMsRepository()

# GET /llms - Get all LLMs.
def get_llms():
    try:
        return repo.get_all(), 200
    except Exception as error:
        return f"Internal server error: {error}", 500

# POST /llms - Create an LLM.
def add_llm():
    try:
        data = request.get_json()

        if data is None:
            return "Body is missing", 400
        
        if not data.get("name"):
            return "Invalid parameters", 400
        
        return repo.add(data), 201
    except Exception as error:
        return f"Internal server error: {error}", 500

# PUT /llms/<id> - Update an LLM by its ID.
def edit_llm(id):
    try:
        data = request.get_json()

        if data is None:
            return "Body is missing", 400
        
        return repo.edit(id, data), 200
    except Exception as error:
        return f"Internal server error: {error}", 500

# DELETE /llms/<id> - Delete an LLM by its ID.
def delete_llm(id):
    try:
        return repo.delete(id), 200
    except Exception as error:
        return f"Internal server error: {error}", 500