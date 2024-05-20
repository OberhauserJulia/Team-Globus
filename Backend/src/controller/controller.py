
from flask import jsonify

def safe_homework(request) : 
     # Zugriff auf den JSON-Body der Anfrage
    if request.is_json:
        data = request.get_json()
        print(data)
    else:
        return jsonify({"error": "Request must be JSON"}), 400


    # Beispielhafte Verarbeitung der Daten
    response_data = {
        "message": "Hello from the controller!",
        "received_data": data
    }
    
    # Response zurückgeben
    return jsonify(response_data), 200
