from app.extensions import db
from app.models import Produto,Historico,Usuario,TipoMovimentacaoEnum
from app.shemas.schemas import MovimentacaoSchema


def registrar_movimentacao(dados: MovimentacaoSchema, usuario_id):
    usuario = db.session.query(Usuario).filter_by(id=usuario_id).first()
    if not usuario:
        raise ValueError('Nao existe esse usuario')
    produto =  db.session.query(Produto).filter_by(id=dados.produto_id).first()
    if not produto:
        raise ValueError('Nao existe esse produto')
    saida = dados.tipo_movimentacao == TipoMovimentacaoEnum.SAIDA
    entrada = dados.tipo_movimentacao == TipoMovimentacaoEnum.ENTRADA
    if saida:
        quantidade_movimentacao = dados.quantidade
        quantidade_estoque = produto.quantidade_estoque
        if quantidade_estoque < quantidade_movimentacao:
            raise ValueError('Quantidade invalida')
        produto.quantidade_estoque -= quantidade_movimentacao
        preco_unitario_produto = produto.preco
        registrar = Historico(preco_unitario=preco_unitario_produto,quantidade_alterada=quantidade_movimentacao,
        usuario_id=usuario_id,produto_id=produto.id,tipo_movimentacao=TipoMovimentacaoEnum.SAIDA)
        db.session.add(registrar)
        db.session.commit()
        return registrar
    elif entrada:
        quantidade_movimentacao = dados.quantidade
        quantidade_estoque = produto.quantidade_estoque
        produto.quantidade_estoque += quantidade_movimentacao
        registrar = Historico(quantidade_alterada=quantidade_movimentacao,
        usuario_id=usuario_id,produto_id=produto.id,tipo_movimentacao=TipoMovimentacaoEnum.ENTRADA)
        db.session.add(registrar)
        db.session.commit()
        return registrar