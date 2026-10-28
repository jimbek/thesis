# Defines the routes for the 'Processes' table.
from crud.repos.ProcessesRepository import ProcessesRepository

from flask import request

# Initialize the ProcessesRepository.
repo = ProcessesRepository()

# GET /processes - Get all Processes.
def get_processes():
    try:
        return repo.get_all(), 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# GET /processes/<id> - Get a Process by its ID.
def get_process_by_id(id):
    try:
        result = repo.get_by_id(id)

        if result is None:
            return {}, 404

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# GET /processes/agent/<id> - Get Processes by their AI Agent ID.
def get_processes_by_agent_id(id):
    try:
        return repo.get_by_agent_id(id), 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# POST /processes - Create a Process.
def add_process():
    try:
        data = request.get_json()
        result = repo.add(data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 201
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# PUT /processes/<id> - Update a Process by its ID.
def edit_process(id):
    try:
        data = request.get_json()
        result = repo.edit(id, data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# DELETE /processes/<id> - Delete a Process by its ID.
def delete_process(id):
    try:
        result = repo.delete(id)
                
        if isinstance(result, dict) and "error" in result:
            return result, 400

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500