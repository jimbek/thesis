# Εδώ δηλώνονται τα routes για τον πίνακα 'Processes'.
from crud.repos.ProcessesRepository import ProcessesRepository

import json
import psutil
import requests
import socket
import subprocess
import time

from flask import request

repo = ProcessesRepository()

# GET /processes.
def get_processes():
    try:
        return repo.get_all(), 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# GET /processes/<id>.
def get_process_by_id(id):
    try:
        result = repo.get_by_id(id)

        if result is None:
            return {}, 404

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# POST /processes.
def add_process():
    try:
        data = request.get_json()
        result = repo.add(data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 201
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# PUT /processes/<id>.
def edit_process(id):
    try:
        data = request.get_json()
        result = repo.edit(id, data)

        if isinstance(result, dict) and "error" in result:
            return result, 400
        
        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# DELETE /processes/<id>.
def delete_process(id: str):
    try:
        result = repo.delete(id)
                
        if isinstance(result, dict) and "error" in result:
            return result, 400

        return result, 200
    except Exception as error:
        return {'error': f"Internal server error: {error}"}, 500

# POST /processes/execute.
def run_process():
    try:
        data = request.get_json()
        if not data:
            return { "error": "Request body is required" }, 400

        # Έλεγχος αν το port δεσμεύεται ήδη
        if __is_port_open__(data.get("port")):
            return { "error": f"Η θύρα {data.get('port')} είναι ήδη σε χρήση." }, 400
        
        payload_as_string = json.dumps(data)
        process = subprocess.Popen(["python", "agent.py", payload_as_string], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")

        # Περιμένουμε μερικά δευτερόλεπτα να σηκωθεί ο server
        server_ready = False
        for _ in range(10):
            time.sleep(2)

            # Έλεγχος αν η διεργασία κρασάρε πρόωρα
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                error_log = stderr if stderr else stdout
                return { "error": f"Ο Flask server κρασάρε κατά την εκκίνηση. Logs:\n{error_log}" }, 500
            
            # Έλεγχος αν άνοιξε η θύρα
            if __is_port_open__(data.get("port")):
                server_ready = True
                break

        # Έλεγχος του αποτελέσματος
        if server_ready:
            return { "pid": process.pid }, 200
        else:
            return { "error": f"Η εντολή απέτυχε. Ο Flask server δεν ήταν έτοιμος στη θύρα {data.get('port')}." }, 500
    except Exception as e:
        return { "error": f"Μήνυμα λάθους (stderr): {e.stderr if hasattr(e, 'stderr') else str(e)}" }, 500

# POST /processes/terminate.
def terminate_process():
    try:
        data = request.get_json()
        if not data:
            return { "error": "Request body is required" }, 400
        
        pid = data.get("pid")
        if pid is None:
            return { "error": "PID is required" }, 400

        psutil.Process(pid).terminate()

        return {}, 200
    except Exception as e:
        return { "error": str(e) }, 500

# POST /processes/chat.
def chat():
    try:
        data = request.get_json()
        if not data:
            return { "error": "Request body is required" }, 400

        port = data.get("port")
        message = data.get("message")
        if port is None or message is None:
            return { "error": "Port and message are required" }, 400

        response = requests.post(f"http://127.0.0.1:{port}/chat", json={"message": message})
        return (response.json(), 200) if response.status_code == 200 else ({ "error": response.text }, response.status_code)
    except Exception as e:
        return { "error": str(e) }, 500

# Checks if a given port is open and the Flask server is ready.
def __is_port_open__(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0