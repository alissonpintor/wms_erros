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
#engine = create_engine('postgresql://alisson:stoky@localhost:5432/alisson')
engineWMS = create_engine('oracle://fullwms:fullwms@192.168.104.4', echo=False)

###############################################################################
# CONFIGURAÇÔES DO CORK #######################################################
###############################################################################
logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

app = bottle.app()

b = SQLiteBackend('database.db', initialize=False)

def populate_backend():
    b.connection.executescript("""
        INSERT INTO users (username, email_addr, desc, role, hash, creation_date) VALUES
        (
            'admin',
            'admin@localhost.local',
            'admin test user',
            'admin',
            'cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=',
            '2012-10-28 20:50:26.286723'
        );
        INSERT INTO roles (role, level) VALUES ('special', 200);
        INSERT INTO roles (role, level) VALUES ('admin', 100);
        INSERT INTO roles (role, level) VALUES ('editor', 60);
        INSERT INTO roles (role, level) VALUES ('user', 50);
    """)
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
