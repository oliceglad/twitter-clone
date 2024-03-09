from app.helpers import start
from app.routes import create_app

app = create_app()

if __name__ == "__main__":
    start()
    app.run(debug=True, host="0.0.0.0", port=7134)
