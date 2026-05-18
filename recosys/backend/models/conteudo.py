from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from backend.database import Base

class Conteudo(Base):
    __tablename__ = "conteudos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    dominio = Column(String, nullable=False)  # filme, musica, curso, produto
    genero = Column(String, nullable=True)
    avaliacao_media = Column(Float, default=0.0)

    interacoes = relationship("Interacao", back_populates="conteudo")
    recomendacoes = relationship("Recomendacao", back_populates="conteudo")
