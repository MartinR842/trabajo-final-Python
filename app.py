from flask import Flask,request,render_template,redirect,url_for,flash
import sqlite3
import csv
app=Flask(__name__)
app.secret_key="cs_1234"

def get_db():
    conn=sqlite3.connect('sociosclub.db')
    conn.row_factory=sqlite3.Row
    return conn

with get_db() as db:
    db.execute("""
            CREATE TABLE IF NOT EXISTS socios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL,
            telefono INTEGER NOT NULL,            
            mail TEXT NOT NULL,
            actividad TEXT NOT NULL      
            )
    """)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar',methods=['GET','POST'])
def agregar():
    if request.method=='POST':
        nombre=request.form['nombre'].strip()
        apellido=request.form['apellido'].strip()
        edad=request.form['edad'].strip()
        telefono=request.form['telefono'].strip()
        mail=request.form['mail'].strip()
        actividad=request.form['actividad'].strip()
        errores=[]
        if len(nombre)<3:
            flash('El nombre debe tener 2 o más caracteres.','error')
            return redirect(url_for('agregar'))
        if len(apellido)<3:
            flash('El apellido debe tener al menos 2 caracteres.','error')
            return redirect(url_for('agregar'))
        if not edad.isdigit():
            flash('para la edad solo se aceptan numeros','error')
            return redirect(url_for('agregar'))
        edad=int(edad)
        if edad <18 or edad>110:
            flash('Ingrese una edad entre 18 y 110')
            return redirect(url_for('agregar'))
        if len(telefono)<1:
            flash('El Telefono es obligaorio no puede estar vacio','error')
            return redirect(url_for('agregar'))
        if len(mail)<1:
            flash('El Correo Electrónico es obligaorio no puede estar vacio','error')
            return redirect(url_for('agregar'))
        if len(actividad)<1:
            flash('La Actividad es obligaorio no puede estar vacio','error')
            return redirect(url_for('agregar'))
        
        if errores:
            for e in errores:
                flash(e,'error')
            return redirect(url_for('agregar'))
        
        with get_db() as db:
            db.execute(
            'INSERT INTO socios(nombre,apellido,edad,telefono,mail,actividad) VALUES(?,?,?,?,?,?)',
            (nombre,apellido,edad,telefono,mail,actividad))
            db.commit()
        with open('socios.txt','a')as f:
            f.write(f'{nombre}-{apellido}-{edad}-{telefono}--{mail}--{actividad}\n')
        with open('socios.csv','a',newline='')as archivo:
            writer= csv.writer(archivo)
            writer.writerow([nombre,apellido,edad,telefono,mail,actividad])
            
        flash('El Socio fue agregado correctamente','success')
        return redirect(url_for('ver_socios'))
    return render_template('agregar.html')

@app.route('/ver')
def ver_socios():
    db=get_db()
    socios= db.execute('SELECT * FROM socios').fetchall()
    return render_template('ver.html',socios=socios)

@app.route('/editar/<int:id>',methods=['GET','POST'])
def editatar(id):
    db=get_db()
    if request.method=='POST':
        nombre=request.form['nombre']
        apellido=request.form['apellido']
        edad=request.form['edad']
        telefono=request.form['telefono']
        mail=request.form['mail']
        actividad=request.form['actividad']
        db.execute("UPDATE socios SET nombre=?,apellido=?,edad=?,telefono=?,mail=?,actividad=? WHERE id=?",
                   (nombre,apellido,edad,telefono,mail,actividad,id))
        db.commit()
        return redirect(url_for('ver_socios'))
    socios=db.execute("SELECT * FROM socios WHERE id=?",(id,)).fetchone()
    return render_template('editar.html',soc=socios)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    db=get_db()
    db.execute('DELETE FROM socios WHERE id=?',(id,))
    db.commit()
    return redirect(url_for('ver_socios'))


if __name__=="__main__":
    app.run(debug=True)

