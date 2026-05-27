from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from blueprints.games import games_bp

def criar_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs",
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "GameVault API",
            "description": "API de catálogo de jogos — projeto acadêmico full stack",
            "version": "1.0.0",
        },
        "basePath": "/",
        "consumes": ["application/json"],
        "produces": ["application/json"],
    }

    Swagger(app, config=swagger_config, template=swagger_template)
    app.register_blueprint(games_bp)

    return app


if __name__ == "__main__":
    app = criar_app()
    print("GameVault API rodando em http://localhost:5000")
    print("Swagger UI disponível em http://localhost:5000/apidocs")
    app.run(debug=True, port=5000)
