from flask import Flask, render_template, request, redirect
import mysql.connector
app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="control_tareas"
    )

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tareas3")
    tareas = cursor.fetchall()
    conn.close()
    return render_template('index.html', actividades=tareas)

@app.route('/add', methods=['POST'])
def add():
    actividad = request.form["actividad"]
    
    # Validaciones
    if not actividad:
        return render_template('index.html', error="El campo de tarea no puede estar vacío.")
    
    if len(actividad) > 100:
        return render_template('index.html', error="La tarea no puede exceder los 100 caracteres.")
    
    # Verificar duplicados
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tareas3 WHERE nombre = %s", (actividad,))
    existing_task = cursor.fetchone()
    if existing_task:
        return render_template('index.html', error="Ya existe una tarea con ese nombre.")
    
    # Insertar nueva tarea
    cursor.execute("INSERT INTO tareas3 (nombre) VALUES (%s)", (actividad,))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas3 WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    actividad = request.form["actividad"]
    
    # Validaciones
    if not actividad:
        return render_template('index.html', error="El campo de tarea no puede estar vacío.")
    
    if len(actividad) > 100:
        return render_template('index.html', error="La tarea no puede exceder los 100 caracteres.")
    
    # Actualizar tarea
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tareas3 SET nombre = %s WHERE id = %s", (actividad, id))
    conn.commit()
    conn.close()
    
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
