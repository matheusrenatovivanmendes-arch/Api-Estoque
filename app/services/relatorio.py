from app.extensions import db
from app.models import Historico,TipoMovimentacaoEnum
from app.shemas.schemas import RelatorioFaturamentoSchema
import pandas as pd
import io

def relatorio(dados: RelatorioFaturamentoSchema):
   vendas = db.session.query(Historico).filter(
    Historico.tipo_movimentacao==TipoMovimentacaoEnum.SAIDA,
    Historico.data_hora.between(dados.data_inicio, dados.data_fim)
    ).all()
   
   resultados = []
   for v in vendas:
       resultados.append({
         'nome': v.produto.nome,
         'quantidade': v.quantidade_alterada,
         'preco':v.preco_unitario,
         'data':v.data_hora,
         'subtotal':v.quantidade_alterada * v.preco_unitario
       })
   df_relatorio = pd.DataFrame(resultados, columns=['nome', 'quantidade', 'preco', 'data', 'subtotal'])
   total = df_relatorio['subtotal'].sum()
   linha_total = pd.DataFrame([{'nome': 'TOTAL', 'subtotal': total}])
   df_final = pd.concat([df_relatorio, linha_total], ignore_index=True)
   buffer = io.BytesIO()             
   df_final.to_excel(buffer, index=False)  
   buffer.seek(0)                     
   return buffer
