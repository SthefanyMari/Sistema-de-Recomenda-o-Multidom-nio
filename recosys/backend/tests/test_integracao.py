import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database import Base, get_db
import uuid
# Banco de dados em memória para testes
DATABASE_TEST_URL = "sqlite:///./test.db"
engine_test = create_engine(DATABASE_TEST_URL, connect_args={"check_same_thread": False})
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)

def override_get_db():
    db = SessionTest()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# ───── Testes de Integração ─────

def test_root():
    """Verifica se a API está respondendo."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "API RecoSys funcionando!"}

def test_cadastro_usuario():
    email = f"{uuid.uuid4()}@teste.com"

    response = client.post("/auth/cadastro", json={
        "nome": "Sthefany Teste",
        "email": email,
        "senha": "senha123"
    })

    assert response.status_code == 200
    assert response.json()["email"] == email

def test_cadastro_email_duplicado():
    """Verifica se o sistema rejeita e-mail já cadastrado."""
    client.post("/auth/cadastro", json={
        "nome": "Usuario Duplicado",
        "email": "duplicado@teste.com",
        "senha": "senha123"
    })
    response = client.post("/auth/cadastro", json={
        "nome": "Usuario Duplicado 2",
        "email": "duplicado@teste.com",
        "senha": "senha456"
    })
    assert response.status_code == 400

def test_login_sucesso():
    """Verifica se o login retorna um token JWT válido."""
    client.post("/auth/cadastro", json={
        "nome": "Login Teste",
        "email": "login@teste.com",
        "senha": "senha123"
    })
    response = client.post("/auth/login", json={
        "email": "login@teste.com",
        "senha": "senha123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_senha_errada():
    """Verifica se o login é recusado com senha incorreta."""
    response = client.post("/auth/login", json={
        "email": "login@teste.com",
        "senha": "senhaerrada"
    })
    assert response.status_code == 401

def test_criar_conteudo():
    """Verifica se um conteúdo pode ser cadastrado com sucesso."""
    response = client.post("/conteudos/", json={
        "titulo": "Interestelar",
        "descricao": "Filme de ficção científica",
        "dominio": "filme",
        "genero": "Ficção Científica"
    })
    assert response.status_code == 200
    assert response.json()["titulo"] == "Interestelar"

def test_listar_conteudos():
    """Verifica se a listagem de conteúdos retorna corretamente."""
    response = client.get("/conteudos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
