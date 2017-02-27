#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, Float, Numeric, Date, ForeignKey
from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship, backref
from app import Base
from datetime import datetime

class Tarefas(Base):
	__tablename__ = 'tarefas'
	id_tarefa = Column(Integer, primary_key=True)
	descricao = Column(String(100), nullable=False)

	def __init__(self, descricao):
		self.descricao = descricao

	def __repr__(self):
		return 'ID: %d - DESCRICAO: %s' % (self.id_tarefas, self.descricao)

class Erros(Base):
	__tablename__ = 'erros'
	id_erro = Column(Integer, primary_key=True)
	descricao = Column(String(100), nullable=False)
	id_tarefa = Column(Integer(), ForeignKey('tarefas.id_tarefa'), nullable=False)

	tarefa = relationship("Tarefas", backref=backref('id_erro', order_by=descricao))

	def __init__(self, descricao, tarefa):
		self.descricao = descricao
		self.id_tarefa = tarefa

	def __repr__(self):
		return 'ID: %d - DESCRICAO: %s' % (self.id_erro, self.descricao)

class RegistroDeErros(Base):
	__tablename__ = 'registro_de_erros'
	id_registro = Column(Integer, primary_key=True)
	id_onda = Column(Integer, nullable=False)
	id_tarefa = Column(Integer, nullable=True)
	cliente = Column(String(100), nullable=False)
	id_produto = Column(String(10), nullable=False)
	id_erro = Column(Integer(), ForeignKey('erros.id_erro'),nullable=False)
	descricao_produto = Column(String(100), nullable=False)
	colaborador = Column(String(45), nullable=True)
	data_cadastro = Column(Date(), default=datetime.now())

	erro = relationship("Erros", backref=backref('id_registro', order_by=colaborador))
