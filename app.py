import log
import secrets
import os
import inspect
from flask import Flask, render_template, request, session, redirect, url_for, flash


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def log_site(site):
    client_ip = request.remote_addr
    log.write(f"Se abrió la página {site} desde: {client_ip}")

@app.route('/')
def home():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('index.html')

@app.route('/estructura')
def estructura():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('estructura.html')

@app.route('/estructura/procesamiento')
def procesamiento():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('procesamiento.html')

@app.route('/estructura/memoria')
def memoria():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('memoria.html')

@app.route('/estructura/memoria/almacenamiento')
def almacenamiento():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('almacenamiento.html')

@app.route('/estructura/memoria/calculo')
def calculo():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('calculo.html')

@app.route('/estructura/perifericos')
def perifericos():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('perifericos.html')

@app.route('/estructura/perifericos/entrada')
def entrada():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('entrada.html')

@app.route('/estructura/perifericos/salida')
def salida():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('salida.html')

@app.route('/diagramas')
def diagramas():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('diagramas.html')

@app.route('/diagramas/flujo')
def flujo():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('flujo.html')

@app.route('/diagramas/bloque')
def bloque():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('bloque.html')

@app.route('/about')
def about():
    log_site(inspect.currentframe().f_code.co_name)
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404  # Renderiza la plantilla 404.html


if __name__ == '__main__':
    set_debug = True
    log.initialize_log(set_debug)
    app.run(debug=set_debug, use_reloader=True)
