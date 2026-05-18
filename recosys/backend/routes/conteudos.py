from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.conteudo import Conteudo
from backend.models.interacao import Interacao
from backend.schemas.conteudo_schema import ConteudoCreate, ConteudoResponse, InteracaoCreate
from typing import List

router = APIRouter(prefix="/conteudos", tags=["Conteúdos"])

@router.get("/", response_model=List[ConteudoResponse])
def listar_conteudos(dominio: str = None, db: Session = Depends(get_db)):
    query = db.query(Conteudo)
    if dominio:
        query = query.filter(Conteudo.dominio == dominio)
    return query.all()

@router.get("/{conteudo_id}", response_model=ConteudoResponse)
def buscar_conteudo(conteudo_id: int, db: Session = Depends(get_db)):
    conteudo = db.query(Conteudo).filter(Conteudo.id == conteudo_id).first()
    if not conteudo:
        raise HTTPException(status_code=404, detail="Conteúdo não encontrado.")
    return conteudo

@router.post("/", response_model=ConteudoResponse)
def criar_conteudo(conteudo: ConteudoCreate, db: Session = Depends(get_db)):
    novo = Conteudo(**conteudo.model_dump())

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo

@router.post("/avaliar")
def avaliar_conteudo(interacao: InteracaoCreate, usuario_id: int, db: Session = Depends(get_db)):
    conteudo = db.query(Conteudo).filter(Conteudo.id == interacao.conteudo_id).first()
    if not conteudo:
        raise HTTPException(status_code=404, detail="Conteúdo não encontrado.")
    nova_interacao = Interacao(
        usuario_id=usuario_id,
        conteudo_id=interacao.conteudo_id,
        avaliacao=interacao.avaliacao
    )
    db.add(nova_interacao)
    db.commit()
    return {"mensagem": "Avaliação registrada com sucesso."}
