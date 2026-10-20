# Describes the routes for the 'Agents' table.
from crud.repos.AgentsRepository import AgentsRepository

from flask import request

# Initialize the AgentsRepository.
repo = AgentsRepository()

# GET /agents - Get all agents.
def get_agents():
    try:
        return repo.get_all(), 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# GET /agents/<id> - Get an agent by its ID.
def get_agent_by_id(id):
    try:
        result = repo.get_by_id(id)

        if result is None:
            return {'error': 'Δεν υπάρχει AI Agent με αυτό το ID.'}, 404

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# POST /agents - Create an agent.
def add_agent():
    try:
        data = request.get_json()
        result = repo.add(data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 201
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# PUT /agents/<id> - Update an agent by its ID.
def edit_agent(id: str):
    try:
        data = request.get_json()
        result = repo.edit(id, data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# DELETE /agents/<id> - Delete an agent by its ID.
def delete_agent(id):
    try:
        result = repo.delete(id)
        
        if isinstance(result, dict) and "error" in result:
            return result, 400

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500