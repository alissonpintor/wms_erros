#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
import bottle
import os

if __name__ == '__main__':
	if os.environ.get('APP_LOCATION') == 'heroku':
		bottle.run(app=app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
	else:
		bottle.run(app=app, host='localhost', port=8889, debug=True, reloader=True)
