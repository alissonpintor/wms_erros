#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bcrypt
from app import app, authorize, aaa
from app.models.tables import Tarefas, Erros, RegistroDeErros
from app.models.tables_wms import WmsOnda, WmsItems, WmsSeparadoresTarefas, WmsColaborador
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import func, desc
import bottle
from bottle import template, static_file, request, redirect
import json
from datetime import datetime

# INICIO converter classe SQLAlchemy em json ##################################
class AlchemyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj.__class__, DeclarativeMeta):
			# an SQLAlchemy class
			fields = {}
			for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
				data = obj.__getattribute__(field)
				if isinstance(data.__class__, datetime):
					data = data.__str__
					print(data)
				try:
					json.dumps(data) # this will fail on non-encodable values, like other classes
					fields[field] = data
				except TypeError:
					fields[field] = None
			# a json-encodable dict
			return fields
		return json.JSONEncoder.default(self, obj)
# FINAL converter classe SQLAlchemy em json ###################################

# INICIO static routes ########################################################
@bottle.get('/<filename:re:.*\.css>')
def stylesheets(filename):
	return static_file(filename, root='app/static/css')

@bottle.get('/<filename:re:.*\.js>')
def javascripts(filename):
	return static_file(filename, root='app/static/js')

@bottle.get('/<filename:re:.*\.json>')
def javascripts(filename):
	return static_file(filename, root='app/static/json')

@bottle.get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
	return static_file(filename, root='app/static/img')

@bottle.get('/<filename:re:.*\.(eot|ttf|woff|woff2|svg)>')
def fonts(filename):
	return static_file(filename, root='app/static')
# FINAL static routes #########################################################

def getStatus(name, message=None):
	status = {}
	if(name == 'SUCESS'):
		if(message):
			status['message'] = '<strong>Sucesso! </strong>' + message
		else:
			status['message'] = '<strong>Sucesso! </strong> Operação realizada com sucesso.'
		status['cssClass'] = 'alert-success'
		return status
	if(name == 'WARNING'):
		if(message):
			status['message'] = '<strong>Aviso! </strong>' + message
		else:
			status['message'] = '<strong>Aviso! </strong> A operação não pode ser realizada'
		status['cssClass'] = 'alert-warning'
		return status
	if(name == 'ERROR'):
		if(message):
			status['message'] = '<strong>Erro! </strong>' + message
		else:
			status['message'] = '<strong>Erro! </strong> Erro ao tentar realizar a operação.'
		status['cssClass'] = 'alert-danger'
		return status

# GERENCIAMENTO DO GRAFICOS ###################################################
@bottle.route('/charts')
@bottle.route('/charts/<option>')
def chrats(db, option=False):
	aaa.require(fail_redirect='/login')

	if option:
		from json import dumps
		from bottle import response

		erros = db.query(RegistroDeErros.colaborador, func.count(RegistroDeErros.id_onda).label('erros_count')).all()
		e_json = {
			'chart': {
				"caption": "Monthly",
				"xaxisname": "Colaboradores",
				"yaxisname": "Erros",
				"showvalues": "1",
				"animation": "1"
			},
			'data': [],
		    "trendlines": [{
		        "line": [{
		            "startvalue": "0",
		            "istrendzone": "1",
		            "valueonright": "1",
		            "tooltext": "AYAN",
		            "endvalue": "30",
		            "color": "009933",
		            "displayvalue": "Target",
		            "showontop": "1",
		            "thickness": "5"
		        }]
		    }]
		}

		for e in erros:
			e_json['data'].append({'label': e.colaborador, 'value':e.erros_count})

		response.content_type = 'application/json'
		return dumps(e_json)
	else:
		user_logged = not aaa.user_is_anonymous
		return template('layout_charts', user_logged=user_logged)

# GERENCIAMENTO DO ERROS DOS FUNCIONARIOS #####################################
@bottle.route('/erros_registrados')
def erros_registrados(db):
	aaa.require(fail_redirect='/login')
	user_logged = not aaa.user_is_anonymous
	return template('layout_erros_registrados', user_logged=user_logged)

@bottle.route('/buscar_erros_registrados', method="GET")
def buscar_erros_registrados(db):
	aaa.require(fail_redirect='/login')
	from json import dumps
	from bottle import response

	limit = request.query.get('limit')
	offset = request.query.get('offset')
	search = request.query.get('search')
	sort = request.query.get('sort')
	order = request.query.get('order')

	r_json = {'total': 0, 'rows': []}

	if(limit and offset):
		registros = db.query(RegistroDeErros)

		if search:
			registros = registros.filter(RegistroDeErros.cliente.like("%{}%".format(search)))
		if sort:
			if order == 'desc':
				registros = registros.order_by(desc(getattr(RegistroDeErros, sort)))
			else:
				registros = registros.order_by(getattr(RegistroDeErros, sort))

		registros = registros.limit(limit)
		registros = registros.offset(offset)

		r_json['total'] = db.query(func.count(RegistroDeErros.id_registro)).first()

		for r in registros:
			r_json['rows'].append({
				'id_registro': r.id_registro,
				'id_onda': r.id_onda,
				'cliente': r.cliente.capitalize(),
				'id_produto': r.id_produto,
				'tipo_tarefa': r.erro.tarefa.descricao,
				'erro': r.erro.descricao,
				'descricao_produto': r.descricao_produto.capitalize(),
				'colaborador': r.colaborador,
				'data_cadastro': str(r.data_cadastro),
			})

	response.content_type = 'application/json'
	return dumps(r_json)

# GERENCIAMENTO DO ERROS ######################################################
@bottle.route('/')
def informar_erros(db):

	tarefas = db.query(Tarefas).join(Erros).all()

	user_logged = not aaa.user_is_anonymous

	'''
	if not user_logged:
		erros = db.query(Erros).filter(Erros.descricao.like('Separa%')).all()
	else:
		erros = db.query(Erros).all()
	'''
	erros = db.query(Erros).all()

	return template('layout_informar_erros', status=False, erros=erros, tarefas=tarefas, user_logged=user_logged)

@bottle.route('/buscar_pedido', method="GET")
def buscar_pedido(wms):
	from json import dumps
	from bottle import response

	id = request.query.get('onda')

	nome = None
	try:
		onda = wms.query(WmsOnda).filter(WmsOnda.id == id)[0]
		nome = onda.nomeCliente
	except IndexError:
		if wms.query(WmsSeparadoresTarefas).filter(WmsSeparadoresTarefas.id == id)[0]:
			nome = 'TAREFA'
	response.content_type = 'application/json'
	return dumps(nome)

@bottle.route('/buscar_produto', method="GET")
def buscar_produto(wms):
	from json import dumps
	from bottle import response

	id = request.query.get('id-produto')
	produto = wms.query(WmsItems).filter(WmsItems.idCiss == id)[0]
	response.content_type = 'application/json'
	return dumps(produto.descricao)

@bottle.route('/colaboradores', method="GET")
def buscar_colaborador_all(wms):
	from json import dumps
	from bottle import response

	result = wms.query(WmsColaborador).all()

	col_j = []
	for c in result:
		col_j.append('%d %s' % (c.id, c.nome))
	return dumps(col_j)

@bottle.route('/buscar_colaborador', method="GET")
def buscar_colaborador(wms, db):
	from json import dumps
	from bottle import response

	idOnda = request.query.get('onda')
	idProduto = request.query.get('id-produto')
	idTipoTarefa = request.query.get('tipo-tarefa')

	tarefa = db.query(Tarefas).filter(Tarefas.id_tarefa == idTipoTarefa)[0].descricao

	tipo_tarefa = None
	if(tarefa.lower() == 'separacao'):
		tipo_tarefa = (4, 7) # 4 7
	if(tarefa.lower() == 'conferencia'):
		tipo_tarefa = (1, 10) # 1 10
	if(tarefa.lower() == 'ressuprimento'):
		tipo_tarefa = (5, 16) # 5 16
	if(tarefa.lower() == 'movimentacao'):
		tipo_tarefa = (2, 9, 8) # 2 9 8

	colaborador = wms.query(WmsSeparadoresTarefas).filter(WmsSeparadoresTarefas.idOnda == idOnda)\
												  .filter(WmsSeparadoresTarefas.idTipoTarefa.in_(tipo_tarefa))\
												  .filter(WmsSeparadoresTarefas.idProduto == idProduto).first()
	if not colaborador:
		colaborador = wms.query(WmsSeparadoresTarefas).filter(WmsSeparadoresTarefas.id == idOnda)\
													  .filter(WmsSeparadoresTarefas.idTipoTarefa.in_(tipo_tarefa))\
													  .filter(WmsSeparadoresTarefas.idProduto == idProduto).first()
	response.content_type = 'application/json'
	print(colaborador)
	nome = str(colaborador.idColaborador) + ' - ' + colaborador.nomeColaborador
	return dumps(nome)

@bottle.route('/buscar_erros/<id_tarefa>', method="GET")
def buscar_erros(db, id_tarefa):
	from json import dumps
	from bottle import response

	erros = db.query(Erros).filter_by(id_tarefa = id_tarefa)

	erros_j = []
	for e in erros:
		e_dict = {
			'id': e.id_erro,
			'descricao': e.descricao
		}
		erros_j.append(e_dict)

	response.content_type = 'application/json'
	return dumps(erros_j)

@bottle.route('/registrar_erro', method="POST")
def registrar_erro(db):

	id_onda = request.forms.get('onda')
	id_produto = request.forms.get('id-produto')
	nome_cliente = request.forms.get('cliente')
	desc_produto = request.forms.get('descricao-produto')
	nome_colaborador = request.forms.get('colaborador')
	tipo_tarefa = request.forms.get('tipo-tarefa')
	id_erro = request.forms.get('tipo-erro')

	if(id_onda and id_produto and id_erro and nome_cliente and desc_produto):
		registro = RegistroDeErros(
			id_onda = id_onda,
			cliente = nome_cliente,
			id_produto = id_produto,
			id_erro = id_erro,
			descricao_produto = desc_produto,
			colaborador = nome_colaborador if nome_colaborador else 'NAO POSSUI'
		)
		db.add(registro)
		db.commit()
		status = getStatus('SUCESS', 'Registro cadastrado com sucesso!')
		erros = db.query(Erros).all()
		tarefas = db.query(Tarefas).join(Erros).all()
		user_logged = not aaa.user_is_anonymous
		return template('layout_informar_erros', erros=erros, status=status, tarefas=tarefas, user_logged=user_logged)
	else:
		form = {'id_onda': id_onda, 'id_produto': id_produto, 'id_erro': id_erro}
		status = getStatus('WARNING', 'Preencha todos os campos')
		erros = db.query(Erros).all()
		tarefas = db.query(Tarefas).join(Erros).all()
		user_logged = not aaa.user_is_anonymous
		return template('layout_informar_erros', erros=erros, status=status, form=form, tarefas=tarefas, user_logged=user_logged)



# GERENCIAMENTO DOS TIPOS DE ERROS ############################################
@bottle.route('/exibir_erros')
def exibir_erros(db, status=False):
	aaa.require(fail_redirect='/login')
	erros = db.query(Erros).all()
	tarefas = db.query(Tarefas).all()
	user_logged = not aaa.user_is_anonymous
	return template('layout_erros', err=erros, tarefas=tarefas, status=status, user_logged=user_logged)

@bottle.route('/cadastrar_erros', method='POST')
def cadastrar_erros(db):
	aaa.require(fail_redirect='/login')
	descricao = request.forms.get('descricao')
	tarefa = request.forms.get('tipo-tarefa')
	if descricao and tarefa:
		erro = Erros(descricao, tarefa)
		db.add(erro)
		db.commit()
		erros = db.query(Erros).all()
		tarefas = db.query(Tarefas).all()
		status = getStatus('SUCESS')
		user_logged = not aaa.user_is_anonymous
		return template('layout_erros', err=erros, tarefas=tarefas, status=status, user_logged=user_logged)
	else:
		status = getStatus('WARNING', 'Preencha todos os campos')
		erros = db.query(Erros).all()
		tarefas = db.query(Tarefas).all()
		user_logged = not aaa.user_is_anonymous
		return template('layout_erros', err=erros, tarefas=tarefas, status=status, user_logged=user_logged)

@bottle.route('/exibir_erros/delete/<id>')
def deletar_erros(db, id):
	aaa.require(fail_redirect='/login')
	if(id):
		try:
			erro = db.query(Erros).filter(Erros.id_erro == id)[0]
			db.delete(erro)
			db.commit()
			erros = db.query(Erros).all()
			tarefas = db.query(Tarefas).all()
			status = getStatus('SUCESS')
			user_logged = not aaa.user_is_anonymous
			return template('layout_erros', err=erros, tarefas=tarefas, status=status, user_logged=user_logged)
		except BaseException as e:
			erros = db.query(Erros).all()
			tarefas = db.query(Tarefas).all()
			status = getStatus('ERROR', 'Código nao existe '+e.args[0])
			user_logged = not aaa.user_is_anonymous
			return template('layout_erros', err=erros, tarefas=tarefas, status=status, user_logged=user_logged)

	redirect('/exibir_erros')

@bottle.route('/exibir_erros/alterar', method="POST")
def alterar_erros(db):
	aaa.require(fail_redirect='/login')
	id = request.forms.get('id')
	descricao = request.forms.get('descricao')
	tarefa = request.forms.get('tipo-tarefa')
	if(id and descricao and tarefa):
		try:
			db.query(Erros).filter_by(id_erro=id).update({"descricao": descricao})
			db.commit()
			erros = db.query(Erros).all()
			tarefas = db.query(Tarefas).all()
			status = getStatus('SUCESS')
			user_logged = not aaa.user_is_anonymous
			return template('layout_erros', err=erros, tarefas=tarefas, status=status, user_logged=user_logged)
		except BaseException as e:
			error=e.args
	else:
		status = getStatus('WARNING', 'Preencha todos os campos')
		erros = db.query(Erros).all()
		tarefas = db.query(Tarefas).all()
		user_logged = not aaa.user_is_anonymous
		return template('layout_erros', err=erros, tarefas=tarefas, status=status, user_logged=user_logged)
	redirect('/exibir_erros')

# GERENCIAMENTO DOS TIPOS DE TAREFAS ############################################
@bottle.route('/exibir_tarefas')
def exibir_tarefas(db, status=False):
	aaa.require(fail_redirect='/login')
	tarefas = db.query(Tarefas).all()
	user_logged = not aaa.user_is_anonymous
	return template('layout_tipo_tarefa', tarefas=tarefas, status=status, user_logged=user_logged)

@bottle.route('/cadastrar_tarefas', method='POST')
def cadastrar_tarefas(db):
	aaa.require(fail_redirect='/login')
	descricao = request.forms.get('descricao')
	if descricao:
		tarefa = Tarefas(descricao)
		db.add(tarefa)
		db.commit()
		tarefas = db.query(Tarefas).all()
		status = getStatus('SUCESS')
		user_logged = not aaa.user_is_anonymous
		return template('layout_tipo_tarefa', tarefas=tarefas, status=status, user_logged=user_logged)
	else:
		status = getStatus('WARNING', 'Preencha o campo descrição')
		tarefas = db.query(Tarefas).all()
		user_logged = not aaa.user_is_anonymous
		return template('layout_tipo_tarefa', tarefas=tarefas, status=status, user_logged=user_logged)

@bottle.route('/exibir_tarefas/delete/<id>')
def deletar_tarefas(db, id):
	aaa.require(fail_redirect='/login')
	if(id):
		try:
			tarefa = db.query(Tarefas).filter(Tarefas.id_tarefa == id)[0]
			db.delete(tarefa)
			db.commit()
			tarefas = db.query(Tarefas).all()
			status = getStatus('SUCESS')
			user_logged = not aaa.user_is_anonymous
			return template('layout_tipo_tarefa', tarefas=tarefas, status=status, user_logged=user_logged)
		except BaseException as e:
			tarefas = db.query(Tarefas).all()
			status = getStatus('ERROR', 'Código nao existe '+e.args[0])
			user_logged = not aaa.user_is_anonymous
			return template('layout_tipo_tarefa', tarefas=tarefas, status=status, user_logged=user_logged)

	redirect('/exibir_tarefas')

@bottle.route('/exibir_tarefas/alterar', method="POST")
def alterar_tarefas(db):
	aaa.require(fail_redirect='/login')
	id = request.forms.get('id')
	descricao = request.forms.get('descricao')
	if(id and descricao):
		try:
			db.query(Tarefas).filter_by(id_tarefa=id).update({"descricao": descricao})
			db.commit()
			tarefas = db.query(Tarefas).all()
			status = getStatus('SUCESS')
			user_logged = not aaa.user_is_anonymous
			return template('layout_tipo_tarefa', tarefas=tarefas, status=status, user_logged=user_logged)
		except BaseException as e:
			error=e.args
	else:
		status = getStatus('WARNING', 'Preencha todos os campos')
		tarefas = db.query(Tarefas).all()
		user_logged = not aaa.user_is_anonymous
		return template('layout_tipo_tarefa', tarefas=tarefas, status=status, user_logged=user_logged)



# CONTROLE DE ACESSO POR USUARIO USANDO CORK ##################################
# #  Bottle methods  # #

def postd():
    return bottle.request.forms


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()


@bottle.post('/login')
def login():
    """Authenticate users"""
    username = post_get('username')
    password = post_get('password')
    aaa.login(username, password, success_redirect='/admin', fail_redirect='/login')

@bottle.route('/logout')
def logout():
    aaa.logout(success_redirect='/')

# Admin-only pages

@bottle.route('/admin')
@bottle.view('admin_page')
def admin():
	"""Only admin users can see this"""
	aaa.require(role='admin', fail_redirect='/sorry_page')
	user_logged = not aaa.user_is_anonymous
	return dict(
        current_user=aaa.current_user,
        users=aaa.list_users(),
        roles=aaa.list_roles(),
		user_logged = user_logged
    )


@bottle.post('/create_user')
def create_user():
    try:
        aaa.create_user(postd().username, postd().role, postd().password)
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_user')
def delete_user():
    try:
        aaa.delete_user(post_get('username'))
        return dict(ok=True, msg='')
    except Exception as e:
        print(repr(e))
        return dict(ok=False, msg=e.message)


@bottle.post('/create_role')
def create_role():
    try:
        aaa.create_role(post_get('role'), post_get('level'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_role')
def delete_role():
    try:
        aaa.delete_role(post_get('role'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)

# Static pages

@bottle.route('/login')
@bottle.view('login_form')
def login_form():
    """Serve login form"""
    return {}


@bottle.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'
