import os

from app import create_app
from dotenv import load_dotenv


load_dotenv()

app = create_app()


if __name__ == "__main__":

    port = int(os.getenv("PORT", 5000))

    debug = os.getenv(
        "FLASK_DEBUG",
        "False"
    ).lower() == "true"

    print("-----------------------------------")
    print("       TRANSITFLOW BACKEND")
    print("-----------------------------------")
    print(f"Server running on port {port}")
    print("Health: http://127.0.0.1:5000/api/health")
    print("Buses:  http://127.0.0.1:5000/api/buses/")
    print("-----------------------------------")

    app.run(
        host="127.0.0.1",
        port=port,
        debug=debug
    )