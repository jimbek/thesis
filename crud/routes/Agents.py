# Εδώ δηλώνονται τα routes για τον πίνακα 'Agents'.
from crud.repos.AgentsRepository import AgentsRepository
from crud.repos.ProcessesRepository import ProcessesRepository

from flask import request

repo = AgentsRepository()
processes_repo = ProcessesRepository()

# GET /agents.
def get_agents():
    try:
        return repo.get_all(), 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# GET /agents/<id>.
def get_agent_by_id(id):
    try:
        result = repo.get_by_id(id)

        if result is None:
            return {'error': 'Δεν υπάρχει AI Agent με αυτό το ID.'}, 404

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# GET /agents/<id>/processes.
def get_processes_by_agent_id(id):
    try:
        result = repo.get_by_id(id)
        
        if result is None:
            return {'error': 'Δεν υπάρχει AI Agent με αυτό το ID.'}, 404
        
        return processes_repo.get_by_agent_id(id), 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# POST /agents.
def add_agent():
    try:
        data = request.get_json()
        result = repo.add(data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 201
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# PUT /agents/<id>.
def edit_agent(id: str):
    try:
        data = request.get_json()
        result = repo.edit(id, data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# DELETE /agents/<id>.
def delete_agent(id):
    try:
        result = repo.delete(id)
        
        if isinstance(result, dict) and "error" in result:
            return result, 400

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500