from dotenv import load_dotenv
import os
from app import app

load_dotenv()

port = int(os.getenv('PORT', 8000))

if __name__ == '__main__':
    print("Server starting...")
    app.run(debug=True, host='0.0.0.0', port=port)
    print(f"Server listening at http://localhost:{port}")
