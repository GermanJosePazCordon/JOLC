from os import close
from flask import Flask, redirect, url_for, render_template, request
from grammar import parse
from tablaSimbolos.C3D import C3D
from tablaSimbolos.Entorno import Entorno
import base64

app = Flask(__name__)

tmp_val=''
global parsed_tree

@app.route("/")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def home():
    return render_template('index.html')

@app.route("/analyze", methods=["POST","GET"])
def analyze():
    if request.method == "POST":
        inpt = request.form["inpt"];
        global tmp_val
        tmp_val=inpt
        return redirect(url_for("analyze"))
    else:
        if tmp_val == '':
            return render_template('analyze.html', initial='', input='')
        genAux = C3D()
        genAux.cleanAll()
        gen = genAux.getInstance()
        result = parse(tmp_val)
        global parsed_tree
        parsed_tree = result
        return render_template('analyze.html', initial=tmp_val, input=gen.getCode())

if __name__ == "__main__":
    app.run(debug=True)#para que se actualice al detectar cambios