from pydantic import BaseModel, Field
from app.models import CargoEnum,TipoMovimentacaoEnum
from typing import Optional
from datetime import date


class ProdutoSchema(BaseModel):
    nome: str = Field(max_length=100, min_length=1)
    descricao: Optional[str] = Field(max_length=255, default=None)
    preco: float = Field(gt=0)
    quantidade_estoque: int = Field(ge=0)
    quantidade_minima_estoque: int = Field(ge=0)
    categoria_id: int = Field(ge=1)

class CategoriaSchema(BaseModel):
    nome: str = Field(max_length=100, min_length=1)
    descricao: Optional[str] = Field(max_length=255, default=None)


class ProcurarProdutoSchema(BaseModel):
    nome: str = Field(max_length=100, min_length=1)

class ProcurarCategoriaSchema(BaseModel):
    nome: str = Field(max_length=100, min_length=1)

class AtualizarProdutoSchema(BaseModel):
  nome: str | None = Field(default=None, min_length=1, max_length=100)
  preco: float | None = Field(default=None, gt=0)
  quantidade_estoque: int | None = Field(default=None, ge=0)
  quantidade_minima_estoque: int | None = Field(default=None, ge=0)
  categoria_id: int | None = Field(default=None, gt=0)
  descricao: str | None = Field(default=None, max_length=255)
class ProcurarUsuarioSchema(BaseModel):
    username: str = Field(max_length=100, min_length=1)


class AtualizarCategoriaSchema(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=100)
    descricao: str | None = Field(default=None, max_length=255)


class UsuarioSchema(BaseModel):
    nome: str = Field(max_length=100, min_length=1)
    username: str = Field(max_length=100, min_length=1)
    senha: str = Field(max_length=15, min_length=8)
    cargo: CargoEnum
class AtualizarUsuarioSchema(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=100)
    username: str | None = Field(default=None, min_length=1, max_length=100)
    senha: str | None = Field(default=None, min_length=8, max_length=15)
    cargo: CargoEnum | None = Field(default=None)
class LoginSchema(BaseModel):
    username: str 
    senha: str 

class MovimentacaoSchema(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)
    tipo_movimentacao: TipoMovimentacaoEnum

class RelatorioFaturamentoSchema(BaseModel):
    data_inicio: date
    data_fim: date

