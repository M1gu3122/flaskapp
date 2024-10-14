from flask import Flask, redirect, request,jsonify,render_template, url_for
from flask import session
import os
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
import jwt
import datetime
from datetime import datetime,timezone,timedelta
from functools import wraps


app = Flask(__name__, template_folder=os.path.join('..', 'web', 'templates'), static_folder=os.path.join('..', 'web', 'static'))


CORS(app)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'granjahoy'
app.config['SECRET_KEY'] = '1f297917cc0205a935e6ebd16edfa5af8b97d0524b70c47f4a2f959784954643'

mysql = MySQL(app)

# secret_key = os.urandom(32).hex()
# print(secret_key)




# Definir permisos por rol
ROLE_PERMISSIONS = {
    'administrador': ['administrador', 'trabajador', 'veterinario'],
    'trabajador': ['trabajador'],
    'veterinario': ['veterinario']
}

# Decorador para verificar el token y el rol
# def role_required(roles):
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             token = None
#             if 'Authorization' in request.headers:
#                 token = request.headers.get('Authorization')
#                 if token and token.startswith('Bearer '):
#                     token = token[7:]  # Elimina 'Bearer ' del encabezado
            
#             if not token:
#                 # return "<h1>Accesso denegado <br> Inicia sesion primero </h1> style "
#                 return make_response("""   <html>
#         <head>
#             <style>
#                 body { font-family: Arial, sans-serif; text-align: center; background-color: #f0f0f0; }
#                 h1 { color: red; }
#                 p { color: #333; }
#             </style>
#         </head>
#         <body>
#             <h1>Acceso denegado</h1>
#             <p>Inicia sesión primero para acceder a esta página.</p>
#         </body>
#         <script>
#                 setTimeout(function() {
#                     window.location.href = '/login'; // Cambia '/login' por la ruta de tu página de inicio de sesión
#                 }, 3000);
#             </script>
#     </html>
# """, 403)
#                 # return jsonify({'message': 'Token es necesario'}), 403
            
#             try:
#                 data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#                 usuario = data['usuario']
#                 current_role = data['rol']
                
#                 # Verificar si el rol tiene permiso para acceder
#                 if current_role not in roles:
#                     return jsonify({'message': 'No tienes permiso para acceder a esta ruta'}), 403

#             except jwt.ExpiredSignatureError:
#                 return jsonify({'message': 'Token expirado'}), 401
#             except jwt.InvalidTokenError:
#                 return jsonify({'message': 'Token inválido'}), 403
            
#             return f(usuario, *args, **kwargs)
        
#         return wrapper
#     return decorator

# @app.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.json
#         usuario = data.get('usuario')
#         contraseña = data.get('contraseña')

#         cursor = mysql.connection.cursor()
#         cursor.execute("""
#             SELECT usuarios.*, roles.tipo_usuario 
#             FROM usuarios 
#             JOIN roles ON usuarios.id_rol = roles.id_rol 
#             WHERE usuarios.usuario = %s
#         """, (usuario,))
#         user = cursor.fetchone()
#         cursor.close()

#         if user:
#             stored_password = user[4].strip()
#             user_role = user[-1]

#             if stored_password == contraseña.strip():
#                 payload = {
#                     'usuario': usuario,
#                     'rol': user_role,
#                     'exp': datetime.now(timezone.utc) + timedelta(minutes=30)  # Token expires in 30 minutes
#                 }
#                 token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
#                 print(payload)
#                 return jsonify({'token': token, 'rol': user_role})
#             else:
#                 return jsonify({'message': 'Credenciales inválidas'}), 401
#         else:
#             return jsonify({'message': 'Credenciales inválidas'}), 401
#     except Exception as e:
#         print(f"Error en login: {e}")
#         return jsonify({'message': 'Error en el servidor'}), 500
# Define a decorator to check the user's role

# def role_required(roles):
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             if 'rol' not in session:
#                 return jsonify({'message': 'No tienes permiso para acceder a esta ruta'}), 403
#             user_role = session['rol']
#             if user_role not in roles:
#                 return jsonify({'message': 'No tienes permiso para acceder a esta ruta'}), 403
            
#             try:
#                 payload = jwt.decode(session['token'], app.config['SECRET_KEY'], algorithms=['HS256'])
#             except jwt.ExpiredSignatureError:
#                 return jsonify({'error': 'token_expired'}), 401
#             except jwt.InvalidTokenError:
#                 return jsonify({'error': 'invalid_token'}), 401
            
#             # Resto de la función
#             return f(*args, **kwargs)
#         return wrapper
#     return decorator
# Define routes


def role_required(roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'rol' not in session or 'token' not in session:
                # return jsonify({'message': 'No tienes permiso para acceder a esta ruta'}), 403
                return render_template('error.html'),403
                
            
            user_role = session['rol']
            if user_role not in roles:
                # return jsonify({'message': 'No tienes permiso para acceder a esta ruta'}), 403
                return render_template('error.html'),403
            
            token = session['token']
            
            # Verifica si el token ha sido revocado
            if is_token_revoked(token):
                return jsonify({'error': 'token_revoked'}), 401  # Token ha sido revocado
            
            try:
                # Decodifica el token
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                # return jsonify({'error': 'token_expired'}), 401
                return render_template('error.html'),403
                
            except jwt.InvalidTokenError:
                return jsonify({'error': 'invalid_token'}), 401
            
            return f(*args, **kwargs)
        return wrapper
    return decorator
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        usuario = data.get('usuario')
        contraseña = data.get('contraseña')

        # Verify user credentials
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT usuarios.id_usuario, usuarios.contraseña, roles.tipo_usuario 
            FROM usuarios 
            JOIN roles ON usuarios.id_rol = roles.id_rol 
            WHERE usuarios.usuario = %s
        """, (usuario,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            id_usuario = user[0]  # El id_usuario es el primer valor
            stored_password = user[1].strip()  # La contraseña está en la segunda columna
            user_role = user[2]  # El rol está en la tercera columna

            if stored_password == contraseña.strip():
                payload = {
                    'usuario': usuario,
                    'id':id_usuario,
                    'rol': user_role,
                    'exp': datetime.now(timezone.utc) + timedelta(minutes=30)  # Token expires in 30 minutes
                }
                token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
                session['rol'] = user_role
                session['token']=token
                print("Tiempo de expiración del token:", payload['exp'].strftime("%Y-%m-%d %H:%M:%S"))
                print(token)
                return jsonify({'token': token, 'rol': user_role})
            else:
                return jsonify({'message': 'Credenciales inválidas'}), 401
        else:
            return jsonify({'message': 'Credenciales inválidas'}), 401
    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({'message': 'Error en login'}), 500

def token_has_expired():
    # Lógica para verificar si el token ha caducado
    # ...
    return True  # o False

@app.route('/token-status', methods=['GET'])
def token_status():
    if token_has_expired():
        return jsonify({'expired': True})
    else:
        return jsonify({'expired': False})

@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for('login'))

revoked_tokens = set()

def destroy_token(token):
    """Agrega el token a la lista de revocados."""
    revoked_tokens.add(token)
    print(f'Token revocado: {token}')

revoked_tokens = set()

def destroy_token(token):
    """Agrega el token a la lista de revocados."""
    revoked_tokens.add(token)
    print(f'Token revocado: {token}')
    print(f'Lista de tokens revocados: {revoked_tokens}')

@app.route('/logout', methods=['POST'])
def logout():
    # Revocar el token si es necesario
    token = session.get('token')
    if token:
        print(f'Revocando token: {token}')  # Mensaje de depuración

        destroy_token(token)

        # Verificar si el token ha sido revocado correctamente
        print(f'Verificando token: {token} - Revocado: {is_token_revoked(token)}')

    # Eliminar la sesión del servidor
    session.clear()

    # Invalida la cookie de sesión
    resp = jsonify({'message': 'Sesión cerrada correctamente'})
    resp.set_cookie('session', '', expires=0)  # Elimina la cookie de sesión

    return resp

def is_token_revoked(token):
    """Verifica si el token ha sido revocado."""
    revoked = token in revoked_tokens
    print(f'Verificando token: {token} - Revocado: {revoked}')
    return revoked

# Ruta para crear una granja

@app.route('/login')
def inicio():
    return render_template('login.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/administrador')
@role_required(['administrador'])
def administrador():
    return render_template('administrador.html')

@app.route('/trabajador')
@role_required(['administrador', 'trabajador'])
def trabajador():
    return render_template('trabajador.html')

@app.route('/veterinario')
@role_required(['administrador', 'veterinario'])
def veterinario():
    return render_template('veterinario.html')
@app.route('/crear_granja', methods=['POST'])
def crear_granja():
    try:
        if request.method == 'POST':
            data = request.json  # Obtén los datos JSON enviados desde el cliente
            id_granja = data.get('id_granja')
            nombre_granja = data.get('nombre_granja')
            contraseña = data.get('contraseña')
            
            if not id_granja or not nombre_granja or not contraseña:
                return jsonify({"informacion": "Todos los campos son obligatorios"}), 400
            
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO granja (id_granja, nombre_granja, contraseña) 
                VALUES (%s, %s, %s)
                """, (id_granja, nombre_granja, contraseña))
            mysql.connection.commit()
            cur.close()
            return jsonify({"informacion": "Registro exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500



#### ruta para crear un registro########
@app.route('/add_contact', methods=['POST'])

def add_contact():
    try:
        if request.method == 'POST':
            data = request.json  # Obtén los datos JSON enviados desde el cliente
            id_usuario = data.get('id_usuario')
            nombres = data.get('nombres')
            apellidos = data.get('apellidos')
            edad = data.get('edad')
            sexo = data.get('sexo')
            usuario = data.get('usuario')
            contraseña = data.get('contraseña')
            id_rol = data.get('id_rol')
            
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO usuarios (id_usuario, nombres, apellidos, edad, sexo, usuario, contraseña, id_rol) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_usuario, nombres, apellidos, edad, sexo, usuario, contraseña, id_rol))
            mysql.connection.commit()
            cur.close()
            return jsonify({"informacion": "Registro exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})

#obtiene todos los registros de la tabla usuarios
@cross_origin()
@app.route('/getAll', methods=['GET'])

def getAll():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT u.id_usuario, u.nombres, u.apellidos, u.usuario, u.contraseña, r.tipo_usuario FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol')
        rv = cur.fetchall()
        cur.close()
        payload = []
        for result in rv:
            content = {
                'id_usuario': result[0],
                'nombres': result[1],
                'apellidos': result[2],
                'usuario': result[3],
                'contraseña': result[4],
                'tipo_usuario': result[5] 
            }
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})

    
#obtiene un usuario en especifico de la tabla usuarios    
@app.route('/get_user/<int:id_usuario>', methods=['GET'])
@cross_origin() 
def get_user(id_usuario):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE id_usuario = %s', (id_usuario,))
        result = cur.fetchone()
        cur.close()

        if result:
            user_data = {
                'id_usuario': result[0],
                'nombres': result[1],
                'apellidos': result[2],  
                'usuario': result[3],
                'contraseña': result[4],
                'id_rol': result[5],
                'edad': result[6],
                'sexo': result[7],
            }
            return jsonify(user_data)
        else:
            return jsonify({'informacion': 'Usuario no encontrado'}), 404
    except Exception as e:
        print(e)
        return jsonify({'informacion': str(e)}), 500
    
@app.route('/buscar_usuario/<string:nombre>', methods=['GET'])
@cross_origin() 
def buscar_usuario(nombre):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE nombres LIKE %s and id_rol=2;', ('%' + nombre + '%',) )
        results = cur.fetchall()
        cur.close()

        if results:
            users_data = []
            for result in results:
                user_data = {
                    'id_usuario': result[0],
                    'nombres': result[1],
                    'apellidos': result[2],  
                    'usuario': result[3],
                    'contraseña': result[4],
                    'id_rol': result[5],
                    'edad': result[6],
                    'sexo': result[7],
                }
                users_data.append(user_data)
            return jsonify(users_data)
        else:
            return jsonify({'informacion': 'Usuario no encontrado'}), 404
    except Exception as e:
        print(e)
        return jsonify({'informacion': str(e)}), 500
@app.route('/buscar_usuario_VT/<string:nombre>', methods=['GET'])
@cross_origin() 
def buscar_usuario_VT(nombre):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE nombres LIKE %s and id_rol=3;', ('%' + nombre + '%',) )
        results = cur.fetchall()
        cur.close()

        if results:
            users_data = []
            for result in results:
                user_data = {
                    'id_usuario': result[0],
                    'nombres': result[1],
                    'apellidos': result[2],  
                    'usuario': result[3],
                    'contraseña': result[4],
                    'id_rol': result[5],
                    'edad': result[6],
                    'sexo': result[7],
                }
                users_data.append(user_data)
            return jsonify(users_data)
        else:
            return jsonify({'informacion': 'Usuario no encontrado'}), 404
    except Exception as e:
        print(e)
        return jsonify({'informacion': str(e)}), 500

    

#Ruta para Eliminar un usuario de la tabla usuario
@cross_origin()
@app.route('/delete/<id>', methods=['DELETE'])
def delete_contact(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM usuarios WHERE id_usuario = %s', (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion": "Registro eliminado"}) 
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500
    
    ######### ruta para actualizar################
#actualizar un registro de la tabla usuario
@cross_origin()
@app.route('/update/<id>', methods=['PUT'])
def update_contact(id):
    try:
        data = request.json
        id_usuario = data.get('id_usuario')
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        edad = data.get('edad')
        sexo = data.get('sexo')
        usuario = data.get('usuario')
        contraseña = data.get('contraseña')
        id_rol = data.get('id_rol')
        
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE usuarios
        SET
            
            id_usuario = %s,
            nombres = %s,
            apellidos = %s,
            edad = %s,
            sexo = %s,        
            usuario = %s,
            contraseña = %s,
            id_rol = %s
        WHERE id_usuario = %s
        """, (id_usuario,nombre, apellido,edad,sexo, usuario, contraseña, id_rol, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion": "Registro actualizado"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500
    
#obtiene un reporte especifico por id
@app.route('/get_report/<int:id>', methods=['GET'])

def get_report(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM reportes WHERE id_reporte = %s', (id,))
        rv = cur.fetchone()
        cur.close()
        if rv:
            report = {
                'id_reporte': rv[0],
                'fecha_registro': rv[1].strftime('%Y-%m-%d'),
                'id_lote': rv[2],
                'diagnostico': rv[3],
                'tratamiento_prescrito': rv[4],
                'fecha_inicio_tratamiento': rv[5].strftime('%Y-%m-%d') if rv[5] else None,
                'fecha_fin_tratamiento': rv[6].strftime('%Y-%m-%d') if rv[6] else None,
                'id_usuario': rv[7],
                'estado_general': rv[8],
                'dosis': rv[9],
                'frecuencia_tratamiento': rv[10]
            }
            return jsonify(report)
        else:
            return jsonify({"informacion": "Reporte no encontrado"}), 404
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500

    
#obtener todas las tareas del trabajador
@app.route('/get_all_tasks', methods=['GET'])
def get_all_tasks():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT t.id_tareas,t.descripcion,t.fecha_asignacion, t.estado,u.nombres, u.id_usuario FROM  tareas t JOIN usuarios u  ON t.id_usuario = u.id_usuario ORDER BY t.fecha_asignacion ASC')
        rv = cur.fetchall()
        cur.close()
        payload = [{'id_tarea': row[0], 'descripcion': row[1], 'fecha_asignacion': row[2].strftime('%Y-%m-%d'), 'estado': row[3], 'nombres': row[4], 'id_usuario': row[5]} 
        for row in rv]
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500
#obtener todas las tareas de un trabajador
@app.route('/obtener_tareas_usuario/<int:id>', methods=['GET'])
def obtener_tareas_usuario(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT id_tareas, descripcion, fecha_asignacion, estado FROM tareas WHERE id_usuario = %s  ORDER BY estado desc, fecha_asignacion asc',(id,))
        rv = cur.fetchall()
        cur.close()
        payload = [{'id_tareas': row[0], 'descripcion': row[1], 'fecha_asignacion': row[2].strftime('%Y-%m-%d'), 'estado': row[3]} 
        for row in rv]
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500
#obtener todas las tareas por trabajador
@app.route('/get_user_tasks/<int:id>', methods=['GET'])
def get_user_tasks(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tareas WHERE id_tareas= %s', (id,))
        rv = cur.fetchall()
        cur.close()
        
        # Convertir los resultados a un formato JSON
        payload = [{
            'id_tareas': row[0],
            'descripcion': row[1],
            'fecha_asignacion': row[2].strftime('%Y-%m-%d'),
            'estado': row[3],
            'id_usuario': row[4]
        } for row in rv]
        
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500

    
#### ruta para crear una tarea
@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    try:
        if request.method == 'POST':
            data = request.json  # Obtén los datos JSON enviados desde el cliente
            descripcion = data.get('descripcion')
            fecha_asignacion = data.get('fecha_asignacion')
            estado = data.get('estado')
            id_usuario = data.get('id_usuario')

            # Debug log
            print(f"Descripcion: {descripcion}, Fecha Asignacion: {fecha_asignacion}, Estado: {estado}, Id Usuario: {id_usuario}")

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tareas (descripcion, fecha_asignacion, estado, id_usuario) VALUES (%s, %s, %s, %s)",
                        (descripcion, fecha_asignacion, estado, id_usuario))
            mysql.connection.commit()
            cur.close()  # Asegúrate de cerrar el cursor
            return jsonify({"informacion": "Registro exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
    
    
#eliminar tareas  por id
@app.route('/eliminar_tarea/<id>', methods=['DELETE'])

def delete_task(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM tareas WHERE id_tareas = %s', (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion": "Tarea eliminada"}) 
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500  
    
#Ruta para editar tarea     
@app.route('/editar_tarea/<id>', methods=['PUT'])

def update_task(id):
    try:
        data = request.json
        descripcion = data.get('descripcion')
        fecha_asignacion = data.get('fecha_asignacion')
        estado = data.get('estado')
        id_usuario = data.get('id_usuario')
        
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE tareas
        SET descripcion = %s,
            fecha_asignacion = %s,
            estado = %s,
            id_usuario = %s
        WHERE id_tareas = %s
        """, (descripcion, fecha_asignacion, estado, id_usuario, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion": "Tarea actualizada exitosamente"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500
    
# ruta para contar los registros de la tabla
@app.route('/getcount', methods=['GET'])

def get_count():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) as total FROM usuarios')
        count = cur.fetchone()
        cur.close()
        return jsonify([{'total': count[0]}])
    except Exception as e:
        print(f"Error en get_count: {e}")
        return jsonify({'informacion': 'Ocurrió un error al obtener el conteo.'}), 500

    
#Ruta para crear reporte del veterinario
@app.route('/crear_reporte', methods=['POST'])

def crear_reporte():
    try:
        if request.method == 'POST':
            data = request.json 
            fecha_registro = data.get('fecha_registro')
            id_lote = data.get('id_lote')
            estado_general = data.get('estado_general')
            diagnostico = data.get('diagnostico')
            tratamiento_prescrito = data.get('tratamiento_prescrito')
            dosis = data.get('dosis')
            frecuencia_tratamiento = data.get('frecuencia_tratamiento')
            fecha_inicio_tratamiento = data.get('fecha_inicio_tratamiento')
            fecha_fin_tratamiento = data.get('fecha_fin_tratamiento')
            id_usuario = data.get('id_usuario')
            
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO reportes (
                    fecha_registro, id_lote, estado_general, diagnostico, tratamiento_prescrito,
                    dosis, frecuencia_tratamiento, fecha_inicio_tratamiento, fecha_fin_tratamiento, id_usuario
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (fecha_registro, id_lote, estado_general, diagnostico, tratamiento_prescrito, dosis,
                  frecuencia_tratamiento, fecha_inicio_tratamiento, fecha_fin_tratamiento, id_usuario))
            mysql.connection.commit()
            cur.close()  # Asegúrate de cerrar el cursor
            return jsonify({"informacion": "Reporte registrado exitosamente"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})

#obtener reportes del veterinario
@app.route('/obtener_reportes', methods=['GET'])

def obtener_reportes():
    try:
        cur = mysql.connection.cursor()
        cur.execute('''
            SELECT r.id_reporte, r.id_lote, r.fecha_registro, u.nombres 
            FROM reportes r
            JOIN usuarios u ON r.id_usuario = u.id_usuario
            ORDER BY r.fecha_registro ASC  -- Ordena por fecha_registro de menor a mayor
        ''')
        rv = cur.fetchall()
        cur.close()
        payload = []
        for result in rv:
            content = {
                'id_reporte': result[0],
                'id_lote': result[1],
                'fecha_registro': result[2],
                'nombre': result[3]
            }
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})

    
#actualizar reportes del veterinario
@app.route('/actualizar_reporte/<id>', methods=['PUT'])

def actualizar_reporte(id):
    try:
        data = request.json
        fecha_registro = data.get('fecha_registro')
        id_lote = data.get('id_lote')
        estado_general = data.get('estado_general')
        diagnostico = data.get('diagnostico')
        tratamiento_prescrito = data.get('tratamiento_prescrito')
        dosis = data.get('dosis')
        frecuencia_tratamiento = data.get('frecuencia_tratamiento')
        fecha_inicio_tratamiento = data.get('fecha_inicio_tratamiento')
        fecha_fin_tratamiento = data.get('fecha_fin_tratamiento')
        id_usuario = data.get('id_usuario')

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE reportes
            SET id_usuario = %s,
                fecha_registro = %s,
                id_lote = %s,
                estado_general = %s,
                diagnostico = %s,
                tratamiento_prescrito = %s,
                dosis = %s,
                frecuencia_tratamiento = %s,
                fecha_inicio_tratamiento = %s,
                fecha_fin_tratamiento = %s
            WHERE id_reporte = %s
        """, (id_usuario, fecha_registro, id_lote, estado_general, diagnostico, tratamiento_prescrito, dosis, frecuencia_tratamiento, fecha_inicio_tratamiento, fecha_fin_tratamiento, id))

        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion": "Registro actualizado exitosamente"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500


#editar estado de las tareas del trabajador
@app.route('/editar_estado/<id>', methods=['PUT'])

def editar_estado(id):
    try:
        data = request.json
        estado = data.get('estado')
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE tareas
        SET estado = %s
        WHERE id_tareas = %s
        """, ( estado, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"informacion":  " Estado actualizado exitosamente"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"informacion": "Error al actualizar el Estado"}), 500



#Ruta de buscador de usuarios 
@app.route('/search_users', methods=['GET'])

def search_users():
    try:
        query = request.args.get('query')  # Obtén el parámetro de búsqueda de la URL

        if not query:
            return jsonify({"informacion": "No se proporcionó ningún criterio de búsqueda"}), 400
        
        cur = mysql.connection.cursor()
        # Usa una consulta SQL para buscar usuarios que coincidan con el criterio
        cur.execute("""
            SELECT * FROM usuarios
            WHERE nombres LIKE %s OR apellidos LIKE %s OR usuario LIKE %s
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        rv = cur.fetchall()
        cur.close()

        payload = []
        for result in rv:
            content = {
                'id_usuario': result[0],
                'nombres': result[1],
                'apellidos': result[2],
                'usuario': result[3],
                'contraseña': result[4],
                'id_rol': result[5]
            }
            payload.append(content)

        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)}), 500

#Ruta para contar los galpones del administrador
@cross_origin()
@app.route('/contar_galpones', methods=['GET'])

def contar_galpones():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) as total FROM galpon')
        result = cur.fetchone()
        cur.close()
        return jsonify({'total': result[0]})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})

#Ruta para contar los lotes del administrador
@cross_origin()
@app.route('/contar_lotes', methods=['GET'])

def contar_lotes():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) as total FROM lote')
        result = cur.fetchone()
        cur.close()
        return jsonify({'total': result[0]})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
    
   
#### ruta para crear un galpon ########
@app.route('/add_galpon', methods=['POST'])

def add_galpon():
    try:
        if request.method == 'POST':
            data = request.json  # Obtén los datos JSON enviados desde el cliente
            capacidad = data.get('capacidad')

            aves = data.get('aves')
            
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO galpon (capacidad,aves) 
                VALUES (%s, %s)
                """, (capacidad,aves))
            mysql.connection.commit()
            cur.close()
            return jsonify({"informacion": "Registro exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
    
#Ruta para crear un lote 
@app.route('/add_lote', methods=['POST'])

def add_lote():
    try:
        if request.method == 'POST':
            data = request.json  # Obtén los datos JSON enviados desde el cliente
            
            num_aves = data.get('num_aves')
            fecha_ingreso = data.get('fecha_ingreso')
            id_galpon = data.get('id_galpon')
            
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO lote (num_aves, fecha_ingreso, id_galpon) 
                VALUES (%s, %s, %s)
                """, (num_aves, fecha_ingreso, id_galpon))
            mysql.connection.commit()
            cur.close()
            return jsonify({"informacion": "Registro exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})

#Ruta para agregar huevos
@app.route('/add_huevo', methods=['POST'])

def add_huevo():
    try:
        if request.method == 'POST':
            data = request.json  # Obtén los datos JSON enviados desde el cliente

            cantidad = data.get('cantidad')
            fecha = data.get('fecha')
            id_lote = data.get('id_lote')

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO huevos (cantidad, fecha, id_lote) 
                VALUES (%s, %s, %s)
                """, (cantidad, fecha, id_lote))
            mysql.connection.commit()
            cur.close()
            return jsonify({"informacion": "Registro de huevos exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
    
@app.route('/add_dato_climatico', methods=['POST'])

def add_dato_climatico():
    try:
        if request.method == 'POST':
            data = request.json

            humedad = data.get('humedad')
            temperatura = data.get('temperatura')
            fecha = data.get('fecha')
            id_galpon = data.get('id_galpon')

            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO datos_climaticos (humedad, temperatura, fecha, id_galpon) 
                VALUES (%s, %s, %s, %s)
                """, (humedad, temperatura, fecha, id_galpon))
            mysql.connection.commit()
            cur.close()
            return jsonify({"informacion": "Registro de datos climáticos exitoso"})
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
@cross_origin() 
@app.route('/getGalpones', methods=['GET'])

def getGalpones():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM galpon')
        rv = cur.fetchall()
        cur.close()
        payload = []
        for result in rv:
            content = {
                'id_galpon': result[0],
                'capacidad': result[1],
                'aves': result[2]
            }
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})

@cross_origin()
@app.route('/getLotes', methods=['GET'])

def getLotes():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM lote')
        rv = cur.fetchall()
        cur.close()
        payload = []
        for result in rv:
            content = {
                'id_lote': result[0],
                'num_aves': result[1],
                'fecha_ingreso': result[2].strftime('%Y-%m-%d'),  # Formatear la fecha
                'id_galpon': result[3]
            }
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})

@cross_origin()
@app.route('/getHuevos', methods=['GET'])

def getHuevos():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM huevos')
        rv = cur.fetchall()
        cur.close()
        payload = []
        for result in rv:
            content = {
                'id_recoleccion': result[0],
                'cantidad': result[1],
                'fecha': result[2].strftime('%Y-%m-%d'),  # Formatear la fecha
                'id_lote': result[3]
            }
            payload.append(content)
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
    

@app.route('/editar_lote/<int:id_lote>', methods=['PUT'])

def editar_lote(id_lote):
    try:
        data = request.json
        num_aves = data.get('num_aves')
        fecha_ingreso = data.get('fecha_ingreso')
        id_galpon = data.get('id_galpon')
        
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE lote
        SET num_aves = %s, fecha_ingreso = %s, id_galpon = %s
        WHERE id_lote = %s
        """, (num_aves, fecha_ingreso, id_galpon, id_lote))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"informacion": "Lote actualizado exitosamente"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"informacion": "Error al actualizar el lote"}), 500
    
@app.route('/editar_galpon/<int:id_galpon>', methods=['PUT'])

def editar_galpon(id_galpon):
    try:
        data = request.json
        capacidad = data.get('capacidad')
        aves = data.get('aves')
        
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE galpon
        SET capacidad = %s, aves = %s
        WHERE id_galpon = %s
        """, (capacidad, aves, id_galpon))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({"informacion": "Galpón actualizado exitosamente"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"informacion": "Error al actualizar el galpón"}), 500


    

    
###################################################DASHBOARD##############################################################

# Estadísticas de Producción de Huevos:
# Total de huevos recolectados por lote.
# Total de huevos recolectados por fecha.
@cross_origin()
@app.route('/estadisticas_huevos', methods=['GET'])

def estadisticas_huevos():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT fecha, SUM(cantidad) AS total_huevos FROM huevos GROUP BY fecha')
        rv = cur.fetchall()
        cur.close()
        
        payload = []
        for result in rv:
            content = {
                'fecha': result[0],
                'total_huevos': result[1]
            }
            payload.append(content)
            
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
    
# Estadísticas de Aves por Galpón:
# Número total de aves por galpón.
# Número de galpones con más o menos aves de acuerdo a la capacidad.
    
@cross_origin()
@app.route('/estadisticas_aves', methods=['GET'])

def estadisticas_aves():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT id_galpon, SUM(aves) AS total_aves FROM galpon GROUP BY id_galpon')
        rv = cur.fetchall()
        cur.close()
        
        payload = []
        for result in rv:
            content = {
                'id_galpon': result[0],
                'total_aves': result[1]
            }
            payload.append(content)
            
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
    
# Estadísticas de Lotes:
# Número de lotes por galpón.
# Número total de aves en los lotes por galpón. 
@app.route('/estadisticas_lotes', methods=['GET'])

def estadisticas_lotes():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT id_galpon, COUNT(id_lote) AS numero_lotes, SUM(num_aves) AS total_aves FROM lote GROUP BY id_galpon')
        rv = cur.fetchall()
        cur.close()
        
        payload = []
        for result in rv:
            content = {
                'id_galpon': result[0],
                'numero_lotes': result[1],
                'total_aves': result[2]
            }
            payload.append(content)
            
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
    



    

@app.route('/estadisticas_tareas', methods=['GET'])

def estadisticas_tareas():
    try:
        cur = mysql.connection.cursor()
        
        # Consulta para contar las tareas pendientes por usuario con nombres
        cur.execute('''
            SELECT u.nombres, COUNT(*) AS tareas_pendientes
            FROM tareas t
            JOIN usuarios u ON t.id_usuario = u.id_usuario
            WHERE t.estado = %s
            GROUP BY u.id_usuario, u.nombres
        ''', ('Pendiente',))
        tareas_pendientes = cur.fetchall()
        
        cur.close()
        
        # Formatear resultados
        payload = {
            'tareas_pendientes': [
                {
                    'nombres': result[0],
                    'tareas_pendientes': result[1]
                } for result in tareas_pendientes
            ]
        }
        
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})

    
@app.route('/estadisticas_clima', methods=['GET'])

def estadisticas_clima():
    try:
        cur = mysql.connection.cursor()
        
        # Consulta para obtener el promedio de temperatura y humedad por galpón
        cur.execute('SELECT id_galpon, AVG(temperatura) AS promedio_temperatura, AVG(humedad) AS promedio_humedad FROM datos_climaticos GROUP BY id_galpon')
        promedio_clima = cur.fetchall()
        
        # Consulta para obtener las lecturas climáticas más recientes por galpón
        cur.execute('''SELECT id_galpon, temperatura, humedad, fecha 
                       FROM datos_climaticos 
                       WHERE fecha = (SELECT MAX(fecha) 
                                      FROM datos_climaticos AS sub 
                                      WHERE sub.id_galpon = datos_climaticos.id_galpon)''')
        clima_reciente = cur.fetchall()
        
        cur.close()
        
        # Formatear resultados
        payload = {
            'promedio_clima': [
                {
                    'id_galpon': result[0],
                    'promedio_temperatura': result[1],
                    'promedio_humedad': result[2]
                } for result in promedio_clima
            ],
            'clima_reciente': [
                {
                    'id_galpon': result[0],
                    'temperatura': result[1],
                    'humedad': result[2],
                    'fecha': result[3]
                } for result in clima_reciente
            ]
        }
        
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})


#Diagnosticos mas frecuentes
@app.route('/diagnosticos_vt', methods=['GET'])

def diagnosticos_vt():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT diagnostico, COUNT(*) AS frecuencia FROM reportes GROUP BY diagnostico ORDER BY frecuencia DESC')
        rv = cur.fetchall()
        cur.close()
        
        payload = []
        for result in rv:
            content = {
                'diagnostico': result[0],
                'frecuencia': result[1]
            }
            payload.append(content)
            
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": str(e)})
    






















if __name__ == "__main__":
    app.run(host="0.0.0.0",  port=3000, debug=True)