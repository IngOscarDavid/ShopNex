from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.models import Carrito
from Config.config import conn, db_config

App = FastAPI()

Carritos = []

@App.get('/')
def index():
   return {"message": "Welcome CRUD with FastAPI Carritos"}

@App.get('/Lista-Carritos')
def Carritos():
    cursor = conn.cursor()
    query = "SELECT * FROM carrito"
    cursor.execute(query)
    carritos = cursor.fetchall()
    cursor.close()

    # Definir las claves descriptivas
    keys = ["id", "Codigo_Usuario", "Codigo_Producto", "Nombre", "Precio", "Imagen", "Total"]

    carritos_dict = []
    for carrito in carritos:
        carrito_dict = {}
        for i in range(len(keys)):
            carrito_dict[keys[i]] = carrito[i]
        carritos_dict.append(carrito_dict)

    return JSONResponse(content=carritos_dict)


@App.get('/Carrito/{ID}', response_model=Carrito)
def read_Carrito(ID: str):
    cursor = conn.cursor()
    query = "SELECT * FROM carrito WHERE id=%s"
    cursor.execute(query,(ID,))
    carrito = cursor.fetchone()
    cursor.close()
    if carrito is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
            "id" : carrito[0],
            "Codigo_Usuario" : carrito[1],
            "Codigo_Producto" : carrito[2],
            "Nombre" : carrito[3],
            "Precio" : carrito[4],
            "Imagen" : carrito[5],
            "Total" : carrito[6],
        }

@App.post('/create-Carrito/', response_model=Carrito)
def create_Carrito(carrito : Carrito):
    cursor = conn.cursor()
    query = "INSERT INTO carrito (Codigo_Usuario, Codigo_Producto, Nombre, Precio, Imagen, Total) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (carrito.Codigo_Usuario, carrito.Codigo_Producto, carrito.Nombre, carrito.Precio, carrito.Imagen, carrito.Total))
    conn.commit()
    carrito.id = cursor.lastrowid
    cursor.close()
    return carrito

@App.put('/update-Carrito/{ID}', response_model=Carrito)
def update_Carrito(ID: str, carrito: Carrito):
    cursor = conn.cursor()
    query = "UPDATE carrito SET Codigo_Usuario=%s, Codigo_Producto=%s, Nombre=%s, Precio=%s, Imagen=%s, Total=%s, WHERE id=%s"
    cursor.execute(query, (carrito.Codigo_Usuario, carrito.Codigo_Producto, carrito.Nombre, carrito.Precio, carrito.Imagen, carrito.Total, ID))
    conn.commit()
    cursor.close()
    carrito.id = ID
    return carrito

@App.delete('/delete-Carritos/{ID}')
def delete_carrito(ID: int):
    cursor = conn.cursor()
    query = "DELETE FROM carrito WHERE id=%s"
    carrito = cursor.execute(query, (ID,))
    conn.commit()
    cursor.close()
    return {"mensaje": "Registro eliminado exitosamente"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(App, host="localhost", port=8003)