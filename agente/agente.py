import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from pydantic import ValidationError
from app import create_app
app = create_app()
app.app_context().push()
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


#Categorias
@tool
def tool_criar_categoria(nome: str, descricao: str | None = None) -> str:
    """
    Cria uma nova categoria de produtos no estoque.
    Use quando o usuário pedir pra cadastrar uma categoria nova.
    """
    try:
        from app.shemas.schemas import CategoriaSchema
        from app.services.categoria import criar_categoria
        dados = CategoriaSchema(nome=nome, descricao=descricao)
        categoria = criar_categoria(dados)
        return f"Categoria '{categoria.nome}' criada com sucesso (ID: {categoria.id})."
    except ValidationError as e:
        return f"Não consegui criar a categoria: {e}"
    except ValueError as e:
        return f"Não consegui criar a categoria: {e}"
@tool
def tool_buscar_categoria(nome: str) -> str:
    """
    Busca uma categoria de produtos no estoque pelo nome.
    Use quando o usuário pedir pra buscar uma categoria existente.
    """
    try:
        from app.shemas.schemas import ProcurarCategoriaSchema
        from app.services.categoria import buscar_categoria
        dados = ProcurarCategoriaSchema(nome=nome)
        categoria = buscar_categoria(dados)
        return f"Categoria encontrada: ID: {categoria.id}, Nome: {categoria.nome}, Descrição: {categoria.descricao}"
    except ValidationError as e:
        return f"Não consegui buscar a categoria: {e}"
    except ValueError as e:
        return f"Não consegui buscar a categoria: {e}"
@tool
def tool_listar_categorias() -> str:
    """
    Lista todas as categorias de produtos no estoque.
    Use quando o usuário pedir pra listar todas as categorias.
    """
    from app.services.categoria import categorias_todos
    categorias = categorias_todos()
    if not categorias:
        return "Nenhuma categoria encontrada."
    return "\n".join([f"ID: {categoria.id}, Nome: {categoria.nome}, Descrição: {categoria.descricao}" for categoria in categorias])
@tool
def tool_atualizar_categoria(categoria_id: int, nome: str | None = None, descricao: str | None = None) -> str:
    """
    Atualiza uma categoria de produtos no estoque.
    Use quando o usuário pedir pra atualizar uma categoria existente.
    """
    from app.services.categoria import atualizar_categoria
    campos_para_atualizar = {}
    if nome is not None:
        campos_para_atualizar['nome'] = nome
    if descricao is not None:
        campos_para_atualizar['descricao'] = descricao
    try:
        categoria = atualizar_categoria(categoria_id, campos_para_atualizar)
        return f"Categoria atualizada com sucesso: ID: {categoria.id}, Nome: {categoria.nome}, Descrição: {categoria.descricao}"
    except ValueError as e:
        return f"Não consegui atualizar a categoria: {e}"
@tool
def tool_deletar_categoria(categoria_id: int) -> str:
    """
    Deleta uma categoria de produtos no estoque.
    Use quando o usuário pedir pra deletar uma categoria existente.
    """
    from app.services.categoria import deletar_categoria
    from app.exceptions import RecursoNaoEncontrado, ConflitoDeRecurso 
    try:
        deletar_categoria(categoria_id)
        return f"Categoria com ID {categoria_id} deletada com sucesso."
    except RecursoNaoEncontrado as e:
        return f"Não consegui deletar a categoria: {e}"
    except ConflitoDeRecurso as e:
        return f"Não consegui deletar a categoria: {e}"

#Produtos
@tool
def tool_criar_produto(nome: str, descricao: str, preco: float, quantidade_estoque: int, quantidade_minima_estoque: int, categoria_id: int) -> str:
    """
    Cria um novo produto no estoque.
    Use quando o usuário pedir pra cadastrar um produto novo.
    """
    from app.shemas.schemas import ProdutoSchema
    from app.services.produtos import criar_produto
    try:
        dados = ProdutoSchema(nome=nome, descricao=descricao, preco=preco, quantidade_estoque=quantidade_estoque, quantidade_minima_estoque=quantidade_minima_estoque, categoria_id=categoria_id)
        produto = criar_produto(dados)
        return f"Produto '{produto.nome}' criado com sucesso (ID: {produto.id})."
    except ValidationError as e:
        return f"Não consegui criar o produto: {e}"
    except ValueError as e:
        return f"Não consegui criar o produto: {e}"
@tool
def tool_buscar_produto(nome: str) -> str:
    """
    Busca um produto no estoque pelo nome.
    Use quando o usuário pedir pra buscar um produto existente.
    """
    from app.shemas.schemas import ProcurarProdutoSchema
    from app.services.produtos import buscar_produto
    try:
        dados = ProcurarProdutoSchema(nome=nome)
        produto = buscar_produto(dados)
        return f"Produto encontrado: ID: {produto.id}, Nome: {produto.nome}, Descrição: {produto.descricao}, Preço: {produto.preco}, Quantidade em Estoque: {produto.quantidade_estoque}, Quantidade Mínima em Estoque: {produto.quantidade_minima_estoque}, Categoria ID: {produto.categoria_id}"
    except ValidationError as e:
        return f"Não consegui buscar o produto: {e}"
    except ValueError as e:
        return f"Não consegui buscar o produto: {e}"
@tool
def tool_listar_produtos() -> str:
    """
    Lista todos os produtos no estoque.
    Use quando o usuário pedir pra listar todos os produtos.
    """
    from app.services.produtos import produtos_todos
    produtos = produtos_todos()
    if not produtos:
        return "Nenhum produto encontrado."
    return "\n".join([f"ID: {produto.id}, Nome: {produto.nome}, Descrição: {produto.descricao}, Preço: {produto.preco}, Quantidade em Estoque: {produto.quantidade_estoque}, Quantidade Mínima em Estoque: {produto.quantidade_minima_estoque}, Categoria ID: {produto.categoria_id}" for produto in produtos]) 

@tool
def tool_atualizar_produto(produto_id: int, nome: str | None = None, descricao: str | None = None, preco: float | None = None, quantidade_estoque: int | None = None, quantidade_minima_estoque: int | None = None, categoria_id: int | None = None) -> str:
    """
    Atualiza um produto no estoque.
    Use quando o usuário pedir pra atualizar um produto existente.
    """
    from app.services.produtos import atualizar_produto
    campos_para_atualizar = {}
    if nome is not None:
        campos_para_atualizar['nome'] = nome
    if descricao is not None:
        campos_para_atualizar['descricao'] = descricao
    if preco is not None:
        campos_para_atualizar['preco'] = preco
    if quantidade_estoque is not None:
        campos_para_atualizar['quantidade_estoque'] = quantidade_estoque
    if quantidade_minima_estoque is not None:
        campos_para_atualizar['quantidade_minima_estoque'] = quantidade_minima_estoque
    if categoria_id is not None:
        campos_para_atualizar['categoria_id'] = categoria_id
    try:
        produto = atualizar_produto(produto_id, campos_para_atualizar)
        return f"Produto atualizado com sucesso: ID: {produto.id}, Nome: {produto.nome}, Descrição: {produto.descricao}, Preço: {produto.preco}, Quantidade em Estoque: {produto.quantidade_estoque}, Quantidade Mínima em Estoque: {produto.quantidade_minima_estoque}, Categoria ID: {produto.categoria_id}"
    except ValueError as e:
        return f"Não consegui atualizar o produto: {e}"
@tool
def tool_deletar_produto(produto_id: int) -> str:
    """
    Deleta um produto no estoque.
    Use quando o usuário pedir pra deletar um produto existente.
    """
    from app.services.produtos import deletar_produto
    from app.exceptions import ConflitoDeRecurso
    try:
        deletar_produto(produto_id)
        return f"Produto com ID {produto_id} deletado com sucesso."
    except ValueError as e:
        return f"Não consegui deletar o produto: {e}"
    except ConflitoDeRecurso as e:
        return f"Não consegui deletar o produto: {e}"

#Relatorio
@tool
def tool_gerar_relatorio(data_inicio: str, data_fim: str) -> str:
    """
    Gera um relatório do estoque.
    Use quando o usuário pedir pra gerar um relatório do estoque.
    """
    from app.services.relatorio import relatorio
    from app.shemas.schemas import RelatorioFaturamentoSchema
    try:
        dados = RelatorioFaturamentoSchema(data_inicio=data_inicio, data_fim=data_fim)
        buffer = relatorio(dados)
        caminho = f"agente/relatorios/faturamento_{data_inicio}_a_{data_fim}.xlsx"
        with open(caminho, 'wb') as f:
            f.write(buffer.read())
        return f"Relatório gerado com sucesso! Arquivo salvo em: {caminho}"
    except ValueError as e:
        return f"Não consegui gerar o relatório: {e}"
#Movimentaçao
def criar_tool_registrar_movimentacao(usuario_id: int):
    @tool
    def tool_registrar_movimentacao(produto_id: int, quantidade: int, tipo_movimentacao: str) -> str:
        """
        Registra uma movimentação de estoque (entrada ou saída) para um produto.
        Use quando o usuário pedir pra registrar entrada ou saída de estoque.
        """
        from app.shemas.schemas import MovimentacaoSchema
        from app.services.movimentacao import registrar_movimentacao
        try:
            dados = MovimentacaoSchema(produto_id=produto_id, quantidade=quantidade, tipo_movimentacao=tipo_movimentacao)
            historico = registrar_movimentacao(dados, usuario_id)
            return f"Movimentação registrada com sucesso (ID: {historico.id})."
        except (ValidationError, ValueError) as e:
            return f"Não consegui registrar a movimentação: {e}"
    return tool_registrar_movimentacao

def criar_agente(usuario_id: int):
    tool_registrar_movimentacao = criar_tool_registrar_movimentacao(usuario_id)

    ferramentas = [
        tool_criar_categoria,
        tool_buscar_categoria,
        tool_listar_categorias,
        tool_atualizar_categoria,
        tool_deletar_categoria,
        tool_criar_produto,
        tool_buscar_produto,
        tool_listar_produtos,
        tool_atualizar_produto,
        tool_deletar_produto,
        tool_gerar_relatorio,
        tool_registrar_movimentacao,
    ]
    return create_agent(
        llm,
        tools=ferramentas,
        system_prompt=(
            "Você é um assistente de estoque. "
            "Use as ferramentas disponíveis para responder às perguntas do usuário."
        ),
    )

#Login
from app.services.autentificar import autenticar
if "usuario_id" not in st.session_state:
    st.title("Login")
    username = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        try:
            usuario = autenticar(username, senha)
            st.session_state["usuario_id"] = usuario.id
            st.rerun()
        except ValueError as e:
            st.error(str(e))
    st.stop()
st.title("Assistente Estoque")

chain = criar_agente(usuario_id=st.session_state["usuario_id"])
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# exibe as mensagens na tela
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input()
if prompt :
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando..."):
            resultado = chain.invoke({"messages": [{"role": "user", "content": prompt}]})
            answer = resultado["messages"][-1].content
            st.write(answer)

    st.session_state["messages"].append({"role": "assistant", "content": answer})