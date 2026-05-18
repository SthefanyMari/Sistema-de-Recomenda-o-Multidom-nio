from fastapi import FastAPI
from backend.database import Base, engine
from backend.models import usuario, conteudo, interacao, recomendacao
from backend.routes import auth, conteudos, recomendacoes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Recomendação Multidomínio",
    description="API para recomendação personalizada de filmes, músicas, cursos e produtos.",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(conteudos.router)
app.include_router(recomendacoes.router)

@app.get("/")
def root():
    return {"mensagem": "API RecoSys funcionando!"}
