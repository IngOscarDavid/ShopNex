from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.models import Pedido
from Config.config import conn, db_config

App = FastAPI()

Pedidos = []

@App.get('/')
def index():
   return {"message": "Welcome CRUD with FastAPI Pedidos"}

@App.get('/Lista-Pedidos')
def Pedidos():
    cursor = conn.cursor()
    query = "SELECT * FROM pedidos"
    cursor.execute(query)
    pedidos = cursor.fetchall()
    cursor.close()

    # Definir las claves descriptivas
    keys = ["id", "Direccion", "Estado", "Ubicacion", "Metodo_Pago", "Total_Pagar"]

    pedidos_dict = []
    for pedido in pedidos:
        pedido_dict = {}
        for i in range(len(keys)):
            pedido_dict[keys[i]] = pedido[i]
        pedidos_dict.append(pedido_dict)

    return JSONResponse(content=pedidos_dict)


@App.get('/Pedido/{ID}', response_model=Pedido)
def read_Pedido(ID: str):
    cursor = conn.cursor()
    query = "SELECT * FROM pedidos WHERE id=%s"
    cursor.execute(query,(ID,))
    Pedido = cursor.fetchone()
    cursor.close()
    if Pedido is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
            "id" : Pedido[0],
            "Direccion" : Pedido[1],
            "Estado" : Pedido[2],
            "Ubicacion" : Pedido[3],
            "Metodo_Pago" : Pedido[4],
            "Total_Pagar" : Pedido[5],
        }

@App.post('/create-Pedido/', response_model=Pedido)
def create_Pedido(pedido : Pedido):
    cursor = conn.cursor()
    query = "INSERT INTO pedidos (Direccion, Estado, Ubicacion, Metodo_Pago, Total_Pagar) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (pedido.Direccion, pedido.Estado, pedido.Ubicacion, pedido.Metodo_Pago, pedido.Total_Pagar))
    conn.commit()
    pedido.id = cursor.lastrowid
    cursor.close()
    return pedido

@App.put('/update-Pedido/{ID}', response_model=Pedido)
def update_Pedido(ID: str, pedido: Pedido):
    cursor = conn.cursor()
    query = "UPDATE pedidos SET Direccion=%s, Estado=%s, Ubicacion=%s, Metodo_Pago=%s, Total_Pagar=%s, WHERE id=%s"
    cursor.execute(query, (pedido.Direccion, pedido.Estado, pedido.Ubicacion, pedido.Metodo_Pago, pedido.Total_Pagar, ID))
    conn.commit()
    cursor.close()
    pedido.id = ID
    return pedido

@App.put('/confirmar-Pedido/{ID}', response_model=Pedido)
def update_Pedido(ID: str):
    cursor = conn.cursor()
    query = "UPDATE pedidos SET Estado = 'Aceptado' WHERE id = %s"
    cursor.execute(query, (ID,))
    conn.commit()
    cursor.close()
    return {"id": ID, "Estado": "Ejecutado"}

@App.delete('/delete-pedidos/{ID}', response_model=Pedido)
def delete_pedido(ID: int):
    cursor = conn.cursor()
    query = "DELETE FROM pedidos WHERE id=%s"
    pedido = cursor.execute(query, (ID,))
    conn.commit()
    cursor.close()
    return {"mensaje": "Registro eliminado exitosamente"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(App, host="localhost", port=8001)