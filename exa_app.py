from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Función para obtener la conexión con la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="control_empleados"
    )

# Ruta principal para mostrar los empleados
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    conn.close()
    return render_template('index.html', empleados=empleados)

# Ruta para agregar un nuevo empleado
@app.route('/add', methods=['POST'])
def add():
    nombre = request.form["nombre"]
    cargo = request.form["cargo"]
    salario = request.form["salario"]  # El salario es un varchar (cadena de texto)
    activo = "Sí" if request.form.get("activo") else "No"  # El campo "activo" se maneja como varchar ("Sí" o "No")

    # Validaciones
    if not nombre or not cargo or not salario:
        return render_template('index.html', error="Todos los campos son obligatorios.")
    
    if len(nombre) > 100:
        return render_template('index.html', error="El nombre del empleado no puede exceder los 100 caracteres.")
    
    # Insertar nuevo empleado
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO empleados (nombre, cargo, salario, activo) VALUES (%s, %s, %s, %s)",
        (nombre, cargo, salario, activo)
    )
    conn.commit()
    conn.close()

    return redirect('/')

# Ruta para eliminar un empleado
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
