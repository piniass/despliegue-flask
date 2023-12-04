from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'personajes'

app.config['MYSQL_HOST'] = 'db4free.net'
app.config['MYSQL_USER'] = 'miguel_pinan'
app.config['MYSQL_PASSWORD'] = 'palomeras98'
app.config['MYSQL_DB'] = 'bdd_miguelp'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personajes')
    data = cur.fetchall()
    return render_template('index.html', personajes = data)

@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        alterego = request.form['alterego']
        tipo = request.form['tipo']
        poder = request.form['poder']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO personajes (nombre, `alter-ego`, tipo, poder) VALUES (%s, %s, %s, %s)',
            (nombre, alterego, tipo, poder))


        mysql.connection.commit()
        flash('Personaje insertado correctamente!')
        return redirect(url_for('Index'))

@app.route('/editar/<id>')
def get_personaje(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personajes WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('edit.html', personajes = data[0])

@app.route('/actualizar/<id>' , methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        alterego = request.form['alterego']
        tipo = request.form['tipo']
        poder = request.form['poder']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE personajes
            SET nombre = %s, 
                `alter-ego` = %s, 
                tipo = %s, 
                poder = %s
            WHERE id = %s
            """,(nombre,alterego,tipo,poder,id))
        mysql.connection.commit()
        flash('Personaje actualizado correctamente!')
        return redirect(url_for('Index'))


@app.route('/eliminar/<string:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM personajes WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Personaje eliminado correctamente!')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug=True)