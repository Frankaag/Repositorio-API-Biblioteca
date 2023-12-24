
import sqlite3

def insertar_libros_ejemplo():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    # Inserción de datos de ejemplo
    libros_ejemplo = [
        ('Cien años de soledad', 'Gabriel García Márquez', 1967),
        ('Confesiones', 'San Agustín', 398),
        ('Don Quijote de la Mancha', 'Miguel de Cervantes', 1605)
    ]

    cursor.executemany('INSERT INTO libros (titulo, autor, anio_publicacion) VALUES (?, ?, ?)', libros_ejemplo)

    # Guardar cambios y cerrar la conexión
    conn.commit()
    conn.close()

