from sqlalchemy import Column, String, Integer, Float, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from app import Base
import datetime

class WmsColaborador(Base):
    __tablename__ = 'WMS_COLABORADORES'
    id = Column('COD_COLAB', Integer, primary_key=True)
    nome = Column('NOME', String(100))

    def __repr__(self):
        return 'COD.: %s - NOME: %s' % (self.id, self.nome)

class WmsItems(Base):
    __tablename__ = 'ITEM'
    id = Column('ID', Integer, primary_key=True)
    idCiss = Column('CODIGO', String(10))
    descricao = Column('DESCRICAO', String(100))

    def __repr__(self):
        return 'COD.: %s - DESCRICAO: %s' % (self.idCiss, self.descricao)

class WmsOnda(Base):
    __tablename__ = 'STOKY_ONDAS_POR_CLIENTE'
    id = Column('ONDA_ID', Integer, primary_key=True)
    idPedido = Column('PEDIDO_ID', Integer)
    idCiss = Column('NUM_PEDIDO', String(10))
    nomeCliente = Column('NOME_CLIENTE', String(100))

    def __repr__(self):
        return 'ONDA: %d - PEDIDO: %s' % (self.id, self.idPedido)

class WmsSeparadoresTarefas(Base):
    __tablename__ = 'STOKY_COLABORADOR_POR_TAREFA'
    id = Column('COD_TAREFA_CD', Integer, primary_key=True)
    idOnda = Column('ONDA_ONDA_ID', Integer)
    idProduto = Column('CODIGO', String(10))
    idColaborador = Column('COD_COLAB', Integer, nullable=False)
    nomeColaborador = Column('NOME', String(45), nullable=False)
    idTipoTarefa = Column('TAREFAS_COD_TAREFA', Integer)

    def __init__(self, nomeColaborador):
        self.nomeColaborador = nomeColaborador

    def __repr__(self):
        return 'ID: %d - DESCRICAO: %s' % (self.id, self.nomeColaborador)
