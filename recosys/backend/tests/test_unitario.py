import pytest
from passlib.context import CryptContext
from backend.routes.auth import hash_senha, verificar_senha, criar_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ───── Testes Unitários ─────

def test_hash_senha():
    """Verifica se a senha é corretamente transformada em hash."""
    senha = "minhasenha123"
    resultado = hash_senha(senha)
    assert resultado != senha
    assert isinstance(resultado, str)

def test_verificar_senha_correta():
    """Verifica se a senha original bate com o hash gerado."""
    senha = "minhasenha123"
    hash = hash_senha(senha)
    assert verificar_senha(senha, hash) is True

def test_verificar_senha_incorreta():
    """Verifica se uma senha errada não bate com o hash."""
    hash = hash_senha("minhasenha123")
    assert verificar_senha("senhaerrada", hash) is False

def test_criar_token():
    """Verifica se o token JWT é gerado corretamente."""
    token = criar_token({"sub": "1"})
    assert isinstance(token, str)
    assert len(token) > 0
