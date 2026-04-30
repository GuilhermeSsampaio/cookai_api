# CookAi API

API limpa do CookAi com auth, OAuth Google, receitas e endpoints de IA.

## Requisitos
- Docker e Docker Compose

## Setup rapido
1. Copie o .env.example para .env e preencha as variaveis.
2. Suba os containers:

```bash
docker compose up --build
```

A API sobe em http://localhost:8000.

## Rotas principais
- POST /auth/register
- POST /auth/login
- POST /auth/refresh
- GET /auth/protected
- GET /auth/google
- GET /auth/google/callback
- GET /users/me
- PUT /users/me
- GET /users
- POST /recipes
- GET /recipes
- PUT /recipes/{recipe_id}
- DELETE /recipes/{recipe_id}
- POST /ai/scrap
- POST /ai/search
