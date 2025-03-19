from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Función para obtener la conexión con la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="series"
    )

# Ruta principal para mostrar los animes
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animes")
    tareas = cursor.fetchall()
    conn.close()
    return render_template('index.html', actividades=tareas)

# Ruta para agregar un nuevo anime con su género
@app.route('/add', methods=['POST'])
def add():
    actividad = request.form["actividad"]
    genero = request.form["genero"]
    
    # Validaciones
    if not actividad:
        return render_template('index.html', error="El campo del anime no puede estar vacío.")
    
    if len(actividad) > 100:
        return render_template('index.html', error="El anime no puede exceder los 100 caracteres.")
    
    # Verificar duplicados
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animes WHERE nombre = %s", (actividad,))
    existing_task = cursor.fetchone()
    if existing_task:
        return render_template('index.html', error="Ya existe un anime con ese nombre.")
    
    # Insertar nuevo anime con su género
    cursor.execute("INSERT INTO animes (nombre, genero) VALUES (%s, %s)", (actividad, genero))
    conn.commit()
    conn.close()
    
    return redirect('/')

# Ruta para eliminar un anime
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM animes WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Ruta para actualizar el nombre de un anime
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    actividad = request.form["actividad"]
    
    # Validaciones
    if not actividad:
        return render_template('index.html', error="El campo del anime no puede estar vacío.")
    
    if len(actividad) > 100:
        return render_template('index.html', error="El anime no puede exceder los 100 caracteres.")
    
    # Actualizar nombre del anime
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE animes SET nombre = %s WHERE id = %s", (actividad, id))
    conn.commit()
    conn.close()
    
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
