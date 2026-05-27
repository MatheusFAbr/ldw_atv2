from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from schemas.game_schema import GameSchema

games_bp = Blueprint("games", __name__, url_prefix="/games")

# Dados em memória — lista Python sem banco de dados
_games: list[dict] = [
    {"id": 1, "titulo": "The Witcher 3", "genero": "RPG", "plataforma": "PC", "nota": 9.8},
    {"id": 2, "titulo": "God of War", "genero": "Ação/Aventura", "plataforma": "PS5", "nota": 9.5},
    {"id": 3, "titulo": "Hollow Knight", "genero": "Metroidvania", "plataforma": "PC", "nota": 9.2},
    {"id": 4, "titulo": "Cyberpunk 2077", "genero": "RPG", "plataforma": "PC", "nota": 8.7},
    {"id": 5, "titulo": "Elden Ring", "genero": "Soulslike", "plataforma": "PC", "nota": 9.6},
]
_next_id = 6


@games_bp.get("/")
def listar_games():
    """
    Lista todos os games cadastrados.
    ---
    tags:
      - Games
    responses:
      200:
        description: Lista de games retornada com sucesso
        schema:
          type: object
          properties:
            total:
              type: integer
              example: 5
            games:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  titulo:
                    type: string
                    example: The Witcher 3
                  genero:
                    type: string
                    example: RPG
                  plataforma:
                    type: string
                    example: PC
                  nota:
                    type: number
                    example: 9.8
    """
    return jsonify({"total": len(_games), "games": _games}), 200


@games_bp.get("/<int:game_id>")
def obter_game(game_id: int):
    """
    Retorna um game específico pelo ID.
    ---
    tags:
      - Games
    parameters:
      - name: game_id
        in: path
        type: integer
        required: true
        description: ID do game
        example: 1
    responses:
      200:
        description: Game encontrado
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            titulo:
              type: string
              example: The Witcher 3
            genero:
              type: string
              example: RPG
            plataforma:
              type: string
              example: PC
            nota:
              type: number
              example: 9.8
      404:
        description: Game não encontrado
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Game não encontrado
    """
    game = next((g for g in _games if g["id"] == game_id), None)
    if game is None:
        return jsonify({"erro": "Game não encontrado"}), 404
    return jsonify(game), 200


@games_bp.post("/")
def cadastrar_game():
    """
    Cadastra um novo game.
    ---
    tags:
      - Games
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - titulo
            - genero
            - plataforma
            - nota
          properties:
            titulo:
              type: string
              example: Hades
            genero:
              type: string
              example: Roguelike
            plataforma:
              type: string
              example: PC
            nota:
              type: number
              minimum: 0
              maximum: 10
              example: 9.3
    responses:
      201:
        description: Game cadastrado com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Game cadastrado com sucesso
            game:
              type: object
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            erro:
              type: string
            detalhes:
              type: array
    """
    global _next_id

    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Body JSON inválido ou ausente"}), 400

    try:
        game_validado = GameSchema(**dados)
    except ValidationError as e:
        erros = [
            {"campo": err["loc"][0], "mensagem": err["msg"]}
            for err in e.errors()
        ]
        return jsonify({"erro": "Dados inválidos", "detalhes": erros}), 400

    novo_game = {
        "id": _next_id,
        "titulo": game_validado.titulo,
        "genero": game_validado.genero,
        "plataforma": game_validado.plataforma,
        "nota": game_validado.nota,
    }
    _games.append(novo_game)
    _next_id += 1

    return jsonify({"mensagem": "Game cadastrado com sucesso", "game": novo_game}), 201
