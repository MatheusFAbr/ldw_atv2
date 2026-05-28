# GameVault — Catálogo de Jogos

Projeto acadêmico full stack com backend Flask, interface desktop Flet e landing page estática.

## Tecnologias

| Camada | Tecnologias |
|---|---|
| Backend | Python, Flask, Blueprints, Flasgger (Swagger), Pydantic, Flask-CORS |
| Frontend | Python, Flet, Requests |
| Landing Page | HTML5, CSS3, Tailwind CSS |
| Armazenamento | Lista Python em memória (sem banco de dados) |

## Estrutura do Projeto

```
ldw_atv2/
├── backend/
│   ├── app.py
│   ├── blueprints/
│   │   ├── __init__.py
│   │   └── games.py
│   └── schemas/
│       ├── __init__.py
│       └── game_schema.py
├── frontend/
│   └── main.py
├── landing-page/
│   └── index.html
├── requirements.txt
└── README.md
```

## Instalação

```bash
pip install -r requirements.txt
```

## Como Rodar

### 1. Backend (terminal 1)

```bash
cd backend
python app.py
```

Servidor disponível em: `http://localhost:5000`  
Swagger UI em: `http://localhost:5000/apidocs`

### 2. Frontend (terminal 2)

```bash
cd frontend
python main.py
```

A janela da aplicação abrirá automaticamente.

### 3. Landing Page

Abrir `landing-page/index.html` diretamente no navegador (duplo clique).

## Endpoints da API

### GET /games
Lista todos os games cadastrados.

**Response 200:**
```json
{
  "total": 5,
  "games": [
    { "id": 1, "titulo": "The Witcher 3", "genero": "RPG", "plataforma": "PC", "nota": 9.8 }
  ]
}
```

### GET /games/\<id\>
Retorna um game específico pelo ID.

**Response 200:**
```json
{ "id": 1, "titulo": "The Witcher 3", "genero": "RPG", "plataforma": "PC", "nota": 9.8 }
```

**Response 404:**
```json
{ "erro": "Game não encontrado" }
```

### POST /games
Cadastra um novo game com validação Pydantic.

**Body:**
```json
{
  "titulo": "Hades",
  "genero": "Roguelike",
  "plataforma": "PC",
  "nota": 9.3
}
```

**Validações:**
- `titulo` — obrigatório, não pode ser vazio
- `genero` — obrigatório, não pode ser vazio
- `plataforma` — obrigatória, não pode ser vazia
- `nota` — número entre 0 e 10

**Response 201:**
```json
{ "mensagem": "Game cadastrado com sucesso", "game": { ... } }
```

**Response 400:**
```json
{ "erro": "Dados inválidos", "detalhes": [ { "campo": "nota", "mensagem": "..." } ] }
```

## Landing Page

Abrir `landing-page/index.html` no navegador — apresenta o projeto com:
- Hero section com visual gamer
- Cards explicativos das três camadas
- Documentação dos endpoints
- Guia de instalação passo a passo
- Design dark responsivo com Tailwind CSS
