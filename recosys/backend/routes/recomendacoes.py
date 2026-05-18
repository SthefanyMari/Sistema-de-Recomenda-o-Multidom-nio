from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.recomendacao_service import gerar_recomendacoes

router = APIRouter(prefix="/recomendacoes", tags=["Recomendações"])

@router.get("/{usuario_id}")
def recomendar(usuario_id: int, db: Session = Depends(get_db)):
    recomendacoes = gerar_recomendacoes(usuario_id, db)
    if not recomendacoes:
        return {"mensagem": "Avalie alguns conteúdos para receber recomendações."}
    return recomendacoes
