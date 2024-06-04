from fastapi import FastAPI, HTTPException, Query, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.models import Producto
from Config.config import conn, db_config

App = FastAPI()

Productos = []

@App.get('/')
def index():
   return {"message": "Welcome CRUD with FastAPI Productos"}

@App.get('/Lista-Productos')
def Products():
    cursor = conn.cursor()
    query = "SELECT * FROM productos"
    cursor.execute(query)
    productos = cursor.fetchall()
    cursor.close()

    # Definir las claves descriptivas
    keys = ["id", "Codigo", "Nombre", "Descripcion", "Catalogo", "Precio", "Cantidad", "Imagen", "Descuento"]

    # Construir un diccionario para cada producto
    productos_dict = []
    for producto in productos:
        producto_dict = {}
        for i in range(len(keys)):
            producto_dict[keys[i]] = producto[i]
        productos_dict.append(producto_dict)

    return JSONResponse(content=productos_dict)

@App.get('/Product/{ID}', response_model=Producto)
def read_Product(ID: int):
    cursor = conn.cursor()
    query = "SELECT * FROM productos WHERE id=%s"
    cursor.execute(query,(ID,))
    producto = cursor.fetchone()
    cursor.close()
    print(producto)
    if producto is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
            "id" : producto[0],
            "Codigo" : producto[1],
            "Nombre" : producto[2],
            "Descripcion" : producto[3],
            "Catalogo" : producto[4],
            "Precio" : producto[5],
            "Cantidad" : producto[6],
            "Image" : producto[7],
            "Descuento" : producto[8],
        }

@App.post('/create-Products/', response_model=Producto)
def create_Product(producto : Producto):
    cursor = conn.cursor()
    query = "INSERT INTO productos (Codigo, Nombre, Descripcion, Catalogo, Precio, Cantidad, Image, Descuento ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (producto.Codigo, producto.Nombre, producto.Descripcion, producto.Catalogo, producto.Precio, producto.Cantidad, producto.Image, producto.Descuento))
    conn.commit()
    producto.id = cursor.lastrowid
    cursor.close()
    return producto

@App.put('/update-Products/{ID}', response_model=Producto)
def update_Product(ID: str, producto: Producto):
    cursor = conn.cursor()
    query = "UPDATE productos SET Codigo=%s, Nombre=%s, Descripcion=%s, Catalogo=%s, Precio=%s, Cantidad=%s, Image=%s, Descuento=%s WHERE Codigo=%s"
    cursor.execute(query, (producto.Codigo, producto.Nombre, producto.Descripcion, producto.Catalogo, producto.Precio, producto.Cantidad, producto.Image, producto.Descuento, ID))
    conn.commit()
    cursor.close()
    producto.id = ID
    return producto

@App.delete('/delete-products/{ID}')
def delete_product(ID: str):
    cursor = conn.cursor()
    query = "DELETE FROM productos WHERE id=%s"
    producto = cursor.execute(query, (ID,))
    conn.commit()
    cursor.close()
    return {"mensaje": "Registro eliminado exitosamente"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(App, host="localhost", port=8000)