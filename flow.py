from bottle import *

@route('/')
def front_page():
	return template('index')
	
run(reloader = True)