#import cx_Oracle as o
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import CHAR
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()
engine = create_engine('oracle://fullwms:fullwms@192.168.104.4')

'''
if __name__ == '__main__':
    con = o.connect('fullwms/fullwms@192.168.104.4')
    print(con.version)

    cursor = con.cursor()
    cursor.execute('select * from WMS_CARGOS')

    for result in cursor:
        print(result)
    cursor.close()

    con.close()
'''

class Cargos(Base):
    __tablename__ = 'WMS_CARGOS'
    id = Column('COD_CARGO', Integer, primary_key=True)
    id_empresa = Column('EMPR_CODEMP', Integer)
    descricao = Column('DESCR_CARGO', String(40), nullable=False)

    def __init__(self, descricao):
        self.descricao = descricao

    def __repr__(self):
        return 'ID: %d - DESCRICAO: %s' % (self.id, self.descricao)

class WmsPedidos(Base):
    __tablename__ = 'PEDIDOS'
    id = Column('ID', Integer, primary_key=True)
    idCiss = Column('NUM_PEDIDO', String(10))
    nomeCliente = Column('NOME_CLIENTE', String(100))
    onda = relationship('WmsOnda')

    def __repr__(self):
        return 'ID: %d - CLIENTE: %s' % (self.id, self.nomeCliente)

class WmsOnda(Base):
    __tablename__ = 'STOKY_ONDAS_POR_CLIENTE'
    id = Column('ONDA_ID', Integer, primary_key=True)
    idPedido = Column('PEDIDO_ID', Integer)
    idCiss = Column('NUM_PEDIDO', String(10))
    nomeCliente = Column('NOME_CLIENTE', String(100))

    def __repr__(self):
        return 'ONDA: %d - PEDIDO: %s' % (self.id, self.idPedido)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

se = Session()

pedido = se.query(WmsOnda).filter(WmsOnda.id == 8768)[0]

print(pedido.pedido)
