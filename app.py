from flask import Flask, request, jsonify, g
import sqlite3
from libros import insertar_libros_ejemplo

# Agrega libros a la base de datos
insertar_libros_ejemplo()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['DATABASE'] = 'biblioteca.db'

# Funciones para manejar la base de datos

def obtener_db():
    print("Conectando a la base de datos...")
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def cerrar_db(exception):
    print("Cerrando la conexión a la base de datos...")
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Rutas de la API

@app.route('/libros', methods=['GET'])
def obtener_todos_los_libros():
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()

    libros_json = []
    for libro in libros:
        libro_dict = {
            'id': libro[0],
            'título': libro[1],
            'autor': libro[2],
            'año_publicación': libro[3]
        }
        libros_json.append(libro_dict)

    print(libros_json)  # Agrega esta línea para imprimir la lista de libros

    return jsonify(libros_json)

# Resto de las rutas de la API...

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)




# ... (resto del código)

# Rutas de la API

# Obtener un libro por ID
@app.route('/libros/<int:libro_id>', methods=['GET'])
def obtener_libro(libro_id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM libros WHERE id = ?', (libro_id,))
    libro = cursor.fetchone()
    
    if libro:
        libro_dict = {
            'id': libro[0],
            'título': libro[1],
            'autor': libro[2],
            'año_publicación': libro[3]
        }
        return jsonify(libro_dict)
    else:
        return jsonify({'mensaje': 'Libro no encontrado'}), 404

# Agregar un nuevo libro
@app.route('/libros', methods=['POST'])
def agregar_libro():
    datos_libro = request.get_json()
    
    if 'título' not in datos_libro or 'autor' not in datos_libro or 'anio_publicacion' not in datos_libro:
        return jsonify({'mensaje': 'Datos incompletos'}), 400

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO libros (título, autor, año_publicación) VALUES (?, ?, ?)',
                    (datos_libro['título'], datos_libro['autor'], datos_libro['año_publicación']))
    db.commit()
    
    nuevo_libro_id = cursor.lastrowid
    nuevo_libro_url = f'/libros/{nuevo_libro_id}'
    
    return jsonify({'mensaje': 'Libro agregado correctamente', 'url': nuevo_libro_url}), 201

# Actualizar un libro por ID
@app.route('/libros/<int:libro_id>', methods=['PUT'])
def actualizar_libro(libro_id):
    datos_libro = request.get_json()

    if 'titulo' not in datos_libro or 'autor' not in datos_libro or 'anio_publicacion' not in datos_libro:
        return jsonify({'mensaje': 'Datos incompletos'}), 400
    
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute('''
        UPDATE libros
        SET título = ?, autor = ?, año_publicación = ?
        WHERE id = ?
    ''', (datos_libro['título'], datos_libro['autor'], datos_libro['año_publicación'], libro_id))
    db.commit()
    
    return jsonify({'mensaje': 'Libro actualizado correctamente'})

# Eliminar un libro por ID
@app.route('/libros/<int:libro_id>', methods=['DELETE'])
def eliminar_libro(libro_id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM libros WHERE id = ?', (libro_id,))
    db.commit()
    
    return jsonify({'mensaje': 'Libro eliminado correctamente'})

# ... (resto del código)
