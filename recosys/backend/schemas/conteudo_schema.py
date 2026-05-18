from pydantic import BaseModel, ConfigDict
from typing import Optional

class ConteudoCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    dominio: str
    genero: Optional[str] = None

class ConteudoResponse(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    dominio: str
    genero: Optional[str]
    avaliacao_media: float

    model_config = ConfigDict(from_attributes=True)

class InteracaoCreate(BaseModel):
    conteudo_id: int
    avaliacao: float