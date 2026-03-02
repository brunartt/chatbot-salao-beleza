from flask import Flask
from routes.webhook import webhook_bp
from config.settings import DEBUG

app = Flask(__name__)
app.register_blueprint(webhook_bp)

@app.route("/")
def home():
    return "Servidor do bot funcionando ✅"


if __name__ == "__main__":
    app.run(debug=DEBUG)

    handler = app