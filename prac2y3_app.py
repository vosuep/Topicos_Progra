from flask import Flask,render_template,request,redirect
import mysql.connector
app = Flask(__name__)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user ="root",
        password= "1234",
        database="control_tareas"
    )
@app.route('/')
def home ():
    conn=get_db_connection()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM tareas2")
    tareas= cursor.fetchall()
    conn.close()
    return render_template('index.html',actividades=tareas)

@app.route('/add', methods=['POST'])
def add ():
    conn=get_db_connection()
    cursor= conn.cursor()
    cursor.execute("INSERT INTO tareas2 (nombre) VALUES (%s)",(request.form["actividad"],))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route ('/delete/<int:id>')
def delete(id):
    conn=get_db_connection()
    cursor= conn.cursor()
    cursor.execute("DELETE FROM tareas2 WHERE id=%s",(id,))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route ('/update/<int:id>', methods=['POST'])
def update(id):
    conn=get_db_connection()
    cursor= conn.cursor()
    cursor.execute("UPDATE tareas2 SET nombre=%s WHERE id=%s",(request.form["actividad"],id))
    conn.commit()
    conn.close()
    return redirect('/')