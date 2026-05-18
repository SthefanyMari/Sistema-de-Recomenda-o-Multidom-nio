# Sistema de Recomendação Multidomínio

Plataforma web para recomendação personalizada de filmes, músicas, cursos e produtos.

## Tecnologias
- Python + FastAPI
- PostgreSQL + SQLAlchemy
- HTML, CSS e JavaScript
- Pytest

## Como rodar no Windows

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/recosys.git
cd recosys
```

### 2. Crie o ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados
- Crie um banco no PostgreSQL chamado `recosys`
- Edite o arquivo `.env` com seu usuário e senha do PostgreSQL

### 5. Rode a aplicação
```bash
uvicorn backend.main:app --reload
```

### 6. Acesse a documentação da API
```
http://localhost:8000/docs
```

## Como rodar os testes
```bash
pytest backend/tests/
```
