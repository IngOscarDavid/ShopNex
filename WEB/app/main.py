from flask import Flask, render_template, request, session, redirect, url_for, flash
import requests
import os
from werkzeug.utils import secure_filename
from pathlib import Path

App = Flask(__name__)

App.config['UPLOAD_FOLDER'] = '../app/static/Img'
App.secret_key = '987654321'

@App.route("/")
def Index():
    return "Bienvenido a la WEB de ventas de ShopNeX"

@App.route("/Informacion")
def Informacion():
    return render_template("Index.html")

@App.route("/Inicio")
def Inicio():
    try:
        response = requests.get('http://localhost:8000/Lista-Productos')
        data_productos = response.json()
        data = data_productos[:4]
        session['data_productos'] = data

        return render_template('Index.html', data_productos=data)
    except requests.exceptions.ConnectionError:
        return render_template('IndexError.html', X="Catalogo", Mensaje="No hay informacion de prodcutos insertados nuevos por error de la WEB API ")

@App.route("/Tienda")
def Tienda(page=1, per_page=2):
    try:
        if request.args.get('ID'):
            return render_template('Tienda.html')
        response = requests.get('http://localhost:8000/Lista-Productos')
        data_productos = response.json()
        data = data_productos[:6]

        session['data_productos'] = data

        return render_template('Tienda.html', data_productos=data)
    except requests.exceptions.ConnectionError:
        return render_template('IndexError.html', X="Catalogo", Mensaje="No se puede ver la informacion de producto por error de la WEB API ")

@App.route("/Perfil")
def Perfil():
    data = session.get('data', [])
    return render_template('Perfil.html', View='Admin', K='List', data=data)

@App.route("/Productos")
def Productos():
    data_productos = session.get('data_productos', [])
    return render_template('Perfil.html', View='Admin', K='List', data_productos=data_productos)

@App.route("/Producto")
def Producto():
    Producto = session.get('Producto', [])
    return render_template('Perfil.html', View='Admin', K='Update', Producto=Producto)

@App.route("/Pedidos")
def Pedidos():
    data_pedidos = session.get('data_pedidos', [])
    return render_template('Perfil.html', View='Admin', K='Pedido', data_pedidos=data_pedidos)

@App.route("/Pedido")
def Pedido():
    Pedido = session.get('Pedido', [])
    return render_template('Perfil.html', View='Admin', K='Update', Pedido=Pedido)

@App.route("/ListaPedidosUsuariosview")
def ListaPedidosUsuariosview():
    Pedido = session.get('Pedido', [])
    return render_template('Perfil.html', View='Usuario', K='Pedidos', Pedido=Pedido)

@App.route("/Notificaciones")
def Notificaciones():
    data_notificaciones = session.get('data_notificaciones', [])
    return render_template('Perfil.html', View='Usuario', K='Notif', data_notificaciones=data_notificaciones)

@App.route("/ViewProductos")
def ViewProductos():
    Producto = session.get('Producto', [])
    return render_template('Tienda.html', Producto=Producto)

@App.route("/Carrito")
def Carrito():
    Carrito = session.get('Carrito', [])
    return render_template('Perfil.html', Carrito=Carrito)

@App.route("/QuitarProducto")
def ViewQuitarProducto():
    return render_template('Perfil.html')

# Funcion para registrar usuarios
@App.route("/Registrar", methods=['POST'])
def Registrar():
    try:
        Usuario ={
            "id" : 0,
            "Nombre": request.form['Nombre'],
            "Correo": request.form['Correo'],
            "Pasword": request.form['password'],
            "Identificacion": request.form['Id'],
            "Direccion": request.form['Direccion'],
            "Rol": 1
        }
        
        response = requests.post('http://localhost:8000/create-Usuarios/', json=Usuario)

        if response.status_code == 200:
            # session['User'] = response.json()['Correo']
            # return redirect(url_for('Perfil'))
            return redirect(url_for('Perfil'))
        else:
            return f"Error: {response.status_code}, {response.text}"
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de Autentificacion', 'danger')
        return redirect(url_for('Perfil', View='Admin', K="Perfil"))

# Funcion para iniciar sesion de usuarios
@App.route('/Login', methods=['POST'])
def Login():
    return "No funciona"

# Funcion para registrar nuevo producto
@App.route("/Nuevo-Producto", methods=['POST'])
def NuevoProducto():
    file = request.files['file']
    filename = secure_filename(file.filename)
    base = os.path.dirname(__file__)

    upload_path = os.path.join(base, 'static/Img', filename)

    file.save(upload_path)
    
    try:
        Producto ={
            "id" : 0,
            "Codigo": request.form['Codigo'],
            "Nombre": request.form['Nombre'],
            "Descripcion": request.form['Descripcion'],
            "Catalogo": request.form['Catalogo'],
            "Precio": request.form['Precio'],
            "Cantidad": request.form['Cantidad'],
            "Image": upload_path,
            "Descuento": request.form['Descuento'],
        }
        
        response = requests.post('http://localhost:8000/create-Products/', json=Producto)

        if response.status_code == 200:
            flash('Producto Registrado', 'success')
            return redirect(url_for('Perfil', View='Admin', K='Perfil'))
        else:
            flash('Producto No Registrado', 'danger')
            return redirect(url_for('Perfil', View='Admin', K='Perfil'))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de catalogo', 'danger')
        return redirect(url_for('Perfil', View='Admin', K="Perfil"))

# Funcion para ver los productos
@App.route("/ListaProductos")
def ListaProductos():
    try:
        response = requests.get('http://localhost:8000/Lista-Productos')
        data_productos = response.json()
        session['data_productos'] = data_productos
        return redirect(url_for('Productos', View='Admin', K="List"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de catalogo', 'danger')
        return redirect(url_for('Perfil', View='Admin', K="Perfil"))

# Funcion para ver un solo producto
@App.route("/BuscarProducto/<int:ID>")
def BuscarProducto(ID):
    try:
        response = requests.get(f'http://localhost:8000/Product/{ID}')
        if response.status_code == 200:
            Producto = response.json()
            session['Producto'] = Producto
            return redirect(url_for('Producto', View='Admin', K="Update"))
        else:
            return 'Error al obtener el registro', 404
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de catalogo', 'danger')
        return redirect(url_for('Perfil', View='Admin', K="Perfil"))


# Funcion para editar productos
@App.route("/EditarProductos/<string:ID>", methods=['POST'])
def EditarProductos(ID):
    try:
        Datos ={
            "id" : 0,
            "Codigo": request.form['Codigo'],
            "Nombre": request.form['Nombre'],
            "Descripcion": request.form['Descripcion'],
            "Catalogo": request.form['Catalogo'],
            "Precio": request.form['Precio'],
            "Cantidad": request.form['Cantidad'],
            "Image": request.form['Image'],
            "Descuento": request.form['Descuento'],
        }

        response = requests.put(f'http://localhost:8000/update-Products/{ID}', json=Datos)

        if response.status_code == 200:
            flash('Producto Actualizado', 'success')
            return redirect(url_for('Perfil', View='Admin', K="Perfil"))
        else:
            return 'Error al actualizar el producto', 400
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de catalogo', 'danger')
        return redirect(url_for('Perfil', View='Admin', K="Perfil"))

# Funcion para eliminar producto
@App.route("/EliminarProducto/<int:ID>")
def EliminarProducto(ID):
    try:
        response = requests.delete(f'http://localhost:8000/delete-products/{ID}')
        if response.status_code == 200:
            flash('Producto eliminado exitosamente', 'success')
            return redirect(url_for('Perfil', View='Admin', K="Perfil"))
        else:
            flash('Error al eliminar el producto', 'success')
            return redirect(url_for('Perfil', View='Admin', K="Perfil"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de catalogo', 'danger')
        return redirect(url_for('Perfil', View='Admin', K="Perfil"))

# Funcion para ver los pedidos
@App.route("/ListaPedidos")
def ListaPedidos():
    try:
        response = requests.get('http://localhost:8001/Lista-Pedidos')
        data_pedidos = response.json()
        session['data_pedidos'] = data_pedidos
        return redirect(url_for('Pedidos', View='Admin', K="Pedidos"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de Pedidos', 'danger')
        return redirect(url_for('Perfil', View='Admin', K="Perfil"))

# Funcion para confirmar pedido
@App.route("/ConfirmarPedido/<int:ID>", methods=['GET', 'POST'])
def ConfirmarPedido (ID):
    try:
        response = requests.put(f'http://localhost:8001/confirmar-Pedido/{ID}')
        flash('Pedido exitosamente Confirmado', 'success')
        return redirect(url_for('Perfil', View='Admin', K="Perfil"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API', 'danger')
        return redirect(url_for('Perfil', View='Admin', K="Perfil"))

# Funcion para eliminar pedido
@App.route("/EliminarPedido/<int:ID>", methods=['GET', 'POST'])
def EliminarPedido(ID):
    try:
        response = requests.delete(f'http://localhost:8001/delete-pedidos/{ID}')
        if response.status_code == 200:
            flash('Error al eliminar el pedido', 'success')
            return redirect(url_for('Perfil', View='Admin', K="Perfil"))
        else:
            flash('Pedido eliminado exitosamente', 'success')
            return redirect(url_for('Perfil', View='Admin', K="Perfil"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API', 'danger')
        return redirect(url_for('Perfil', View='Admin', K="Perfil"))

# Funcion para ver las notificaciones de los usuarios
@App.route("/ListNotificaciones")
def ListNotificaciones():
    try:
        response = requests.get('http://localhost:8002/Lista-Notificacion')
        data_notificaciones = response.json()
        session['data_notificaciones'] = data_notificaciones
        return redirect(url_for('Notificaciones', View='Usuario', K="Notif"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API Notificaciones', 'danger')
        return redirect(url_for('Perfil', View='Usuario', K="Perfil"))

# Funcion para ver los pedidos
@App.route("/ListaPedidosUsuarios")
def ListaPedidosUsuarios():
    try:
        response = requests.get('http://localhost:8001/Lista-Pedidos')
        Pedido = response.json()
        session['Pedido'] = Pedido
        return redirect(url_for('ListaPedidosUsuariosview', View='Usuario', K="Pedidos"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de Pedidos', 'danger')
        return redirect(url_for('Perfil', View='Usuario', K="Perfil"))

# Funcion para eliminar pedido
@App.route("/EliminarNoti/<int:ID>", methods=['GET', 'POST'])
def EliminarNoti(ID):
    try:
        response = requests.delete(f'http://localhost:8002/delete-notificacion/{ID}')
        if response.status_code == 200:
            flash('Error al eliminar el pedido', 'success')
            return redirect(url_for('Perfil', View='Usuario', K="Notif"))
        else:
            flash('Pedido eliminado exitosamente', 'success')
            return redirect(url_for('Perfil', View='Usuario', K="Perfil"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de pedidos', 'danger')
        return redirect(url_for('Perfil', View='Usuario', K="Perfil"))

# Funcion para enviar notificaciones
@App.route("/CrearNotificaciones", methods=['POST'])
def CrearNotificaciones():
    try:
        if request.form['Codigo'] == "":
            Codigo = "0"
        else:
            Codigo = request.form['Codigo']
        
        Notificacion = {
            "id" : 0,
            "Codigo_Usuario" : Codigo,
            "Texto" : request.form['Texto'],
            "Estado" : "No Visto"
        }

        response = requests.post('http://localhost:8002/create-Notificacin/', json=Notificacion)

        if response.status_code == 200:
            flash('Notificacion Enviada', 'success')
            return redirect(url_for('Perfil', View='Admin', K='Perfil'))
        else:
            return f"Error: {response.status_code}, {response.text}"

    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de notificaciones', 'danger')
        return redirect(url_for('Perfil', View='Admin', K="Perfil"))

# Funcion para marcar el visto
@App.route("/ConfirmarNotificaciones/<int:ID>/<string:Id_Usuario>", methods=['GET', 'POST'])
def ConfirmarNotificaciones (ID, Id_Usuario):
    try:
        response = requests.put(f'http://localhost:8002/marcar-visto/{ID}/{Id_Usuario}')
        flash('Notificacion marcada vista', 'success')
        return redirect(url_for('Perfil', View='Usuario', K="Perfil"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de notificaciones', 'danger')
        return redirect(url_for('Perfil', View='Usuario', K="Perfil"))

# Funcion para ver un solo producto
@App.route("/BuscarProduct/<int:ID>")
def BuscarProduct(ID):
    try:
        response = requests.get(f'http://localhost:8000/Product/{ID}')
        if response.status_code == 200:
            Producto = response.json()
            session['Producto'] = Producto
            return redirect(url_for('ViewProductos', ID=Producto['id']))
        else:
            return 'Error al obtener el registro', 404
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de catalogo', 'danger')
        return redirect(url_for('Tienda'))

# Funcion para añadir productos al carro de usuario
@App.route("/AñadirProductoACarrito/<int:ID>/<string:Id_Usuario>/")
def AñadirProductoACarrito(ID, Id_Usuario):
    try:
        res = requests.get(f"http://localhost:8000/Product/{ID}")
        Codigo = res.json()
        session['Codigo'] = Codigo

        Car = {
            "id" : 0,
            "Codigo_Usuario" : Id_Usuario,
            "Codigo_Producto" : Codigo['Codigo'],
            "Nombre" : Codigo['Nombre'],
            "Precio" : Codigo['Precio'],
            "Imagen" : Codigo['Image'],
            "Total" : "0"
        }
        response = requests.post("http://localhost:8003/create-Carrito/", json=Car)
        if response.status_code == 200:
            flash('Producto Añadido Al Carrito', 'success')
            return redirect(url_for('Perfil', View='Usuario', K="Perfil"))
        else:
            flash('Producto No Añadido Al Carrito', 'danger')
            return redirect(url_for('Perfil', View='Usuario', K="Perfil"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API De Carritos', 'danger')
        return redirect(url_for('Perfil', View='Usuario', K="Perfil"))

# Funcion para ver los productos añadidos al carrito de un usuario 
@App.route("/VerCarrito")
def VerCarrito():
    try:
        response = requests.get("http://localhost:8003/Lista-Carritos")
        Carrito = response.json()
        session['Carrito'] = Carrito

        return redirect(url_for('Carrito', View='Usuario', K="Carrito"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API De Carritos', 'danger')
        return redirect(url_for('Perfil', View='Usuario', K="Perfil"))

# Funcion para eliminar productos del carrito de los usuarios
@App.route("/QuitarProducto/<int:ID>")
def QuitarProducto(ID):
    try:
        response = requests.delete(f'http://localhost:8003/delete-Carritos/{ID}')
        if response.status_code == 200:
            flash('Producto eliminado del carrito', 'success')
            return redirect(url_for('Perfil', View='Usuario', K="Perfil"))
        else:
            flash('Error a eliminar el producto del carrito', 'danger')
            return redirect(url_for('Perfil', View='Usuario', K="Perfil"))
    except requests.exceptions.ConnectionError:
        flash('Error De WEB API de carritos', 'danger')
        return redirect(url_for('Perfil', View='Usuario', K="Perfil"))

if __name__ == '__main__':
    App.run(host="0.0.0.0", port=4000, debug=True)