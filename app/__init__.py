#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle_session
import bottle
from bottle import Bottle, TEMPLATE_PATH
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from beaker.middleware import SessionMiddleware
from cork import Cork
from cork.backends import SQLiteBackend
import logging


Base = declarative_base()
engine = create_engine('sqlite:///database.db', echo=False)
engineWMS = create_engine('oracle://fullwms:fullwms@192.168.104.4', echo=False)

###############################################################################
# CONFIGURAÇÔES DO CORK #######################################################
###############################################################################
logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

app = bottle.app()

b = SQLiteBackend('database.db', initialize=False)

aaa = Cork(backend=b, email_sender='federico.ceratto@gmail.com', smtp_url='smtp://smtp.magnet.ie')
authorize = aaa.make_auth_decorator(fail_redirect="/login", role="user")

session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}


###############################################################################
# CONFIGURAÇÔES DA PASTA DAS VIEWS ############################################
###############################################################################
bottle.debug(True)
TEMPLATE_PATH.insert(0, 'app/views/')

plugin = sqlalchemy.Plugin(
    engine,
    Base.metadata,
    keyword='db',
    create=True,
    commit=True,
    use_kwargs=False
)

pluginWMS = sqlalchemy.Plugin(
    engineWMS,
    Base.metadata,
    keyword='wms',
    create=False,
    commit=False,
    use_kwargs=False
)

bottle.install(plugin)
bottle.install(pluginWMS)

app = SessionMiddleware(app, session_opts)

from app.controllers import default
from app.models import tables
