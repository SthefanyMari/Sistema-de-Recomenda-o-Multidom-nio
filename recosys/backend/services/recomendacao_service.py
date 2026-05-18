from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.orm import Session
from backend.models.conteudo import Conteudo
from backend.models.interacao import Interacao
from backend.models.recomendacao import Recomendacao

def gerar_recomendacoes(usuario_id: int, db: Session, limite: int = 5):
    # Busca os conteúdos já avaliados pelo usuário
    interacoes = db.query(Interacao).filter(Interacao.usuario_id == usuario_id).all()
    if not interacoes:
        return []

    ids_avaliados = [i.conteudo_id for i in interacoes]

    # Busca todos os conteúdos
    todos_conteudos = db.query(Conteudo).all()
    if not todos_conteudos:
        return []

    # Vetoriza as descrições dos conteúdos
    descricoes = [f"{c.titulo} {c.descricao or ''} {c.genero or ''}" for c in todos_conteudos]
    vectorizer = TfidfVectorizer()
    matriz = vectorizer.fit_transform(descricoes)

    # Calcula a similaridade entre conteúdos avaliados e os demais
    indices_avaliados = [i for i, c in enumerate(todos_conteudos) if c.id in ids_avaliados]
    scores = cosine_similarity(matriz[indices_avaliados], matriz).mean(axis=0)

    # Ordena e filtra os já avaliados
    recomendados = []
    for idx, score in sorted(enumerate(scores), key=lambda x: x[1], reverse=True):
        conteudo = todos_conteudos[idx]
        if conteudo.id not in ids_avaliados:
            recomendados.append({
                "conteudo_id": conteudo.id,
                "titulo": conteudo.titulo,
                "dominio": conteudo.dominio,
                "score": round(float(score), 4),
                "motivo": f"Baseado no seu interesse em {conteudo.genero or conteudo.dominio}"
            })
        if len(recomendados) >= limite:
            break

    # Salva as recomendações no banco
    db.query(Recomendacao).filter(Recomendacao.usuario_id == usuario_id).delete()
    for r in recomendados:
        nova = Recomendacao(
            usuario_id=usuario_id,
            conteudo_id=r["conteudo_id"],
            score=r["score"],
            motivo=r["motivo"]
        )
        db.add(nova)
    db.commit()

    return recomendados
