from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models.models import Notificacion, Not
from Config.config import conn, db_config

App = FastAPI()

Notificaciones = []

@App.get('/')
def index():
   return {"message": "Welcome CRUD with FastAPI Notificacion"}

@App.get('/Lista-Notificacion')
def Notificaiones():
    cursor = conn.cursor()
    query = "SELECT * FROM notificaiones"
    cursor.execute(query)
    notificaiones = cursor.fetchall()
    cursor.close()

    # Definir las claves descriptivas
    keys = ["id", "Codigo_Usuario", "Texto", "Estado"]

    notificaiones_dict = []
    for notificaion in notificaiones:
        notificaion_dict = {}
        for i in range(len(keys)):
            notificaion_dict[keys[i]] = notificaion[i]
        notificaiones_dict.append(notificaion_dict)

    return JSONResponse(content=notificaiones_dict)


@App.get('/Notificacion/{ID}', response_model=Notificacion)
def read_Notificacion(ID: str):
    cursor = conn.cursor()
    query = "SELECT * FROM notificaiones WHERE id=%s"
    cursor.execute(query,(ID,))
    Notificacion = cursor.fetchone()
    cursor.close()
    if Notificacion is None:
        raise HTTPException(status_code=404, detail="Notificacion not found")
    return {
            "id" : Notificacion[0],
            "Codigo_Usuario " : Notificacion[1],
            "Texto" : Notificacion[2],
            "Estado" : Notificacion[3],
        }

@App.post('/create-Notificacin/', response_model=Notificacion)
def create_Notificacion(notificaion : Notificacion):
    cursor = conn.cursor()
    query = "INSERT INTO notificaiones (Codigo_Usuario, Texto, Estado) VALUES (%s, %s, %s)"
    cursor.execute(query, (notificaion.Codigo_Usuario, notificaion.Texto, notificaion.Estado))
    conn.commit()
    notificaion.id = cursor.lastrowid
    cursor.close()
    return notificaion

@App.put('/update-Notificacion/{ID}', response_model=Notificacion)
def update_Pedido(ID: str, notificaion : Notificacion):
    cursor = conn.cursor()
    query = "UPDATE notificaiones SET Codigo_Usuario =%s, Texto=%s, Estado=%s WHERE id=%s"
    cursor.execute(query, (notificaion.Codigo_Usuario, notificaion.Texto, notificaion.Estado, ID))
    conn.commit()
    cursor.close()
    notificaion.id = ID
    return notificaion

@App.put('/marcar-visto/{ID}/{ID_Usuario}', response_model=Not)
def marca_notificacion(ID: int, ID_Usuario: str):
    cursor = conn.cursor()
    query = "UPDATE notificaiones SET Estado = 'Visto' WHERE id = %s AND Codigo_Usuario = %s"
    cursor.execute(query, (ID, ID_Usuario,))
    conn.commit()
    cursor.close()
    return {"id": ID, "Estado": "Ejecutado"}

@App.delete('/delete-notificacion/{ID}', response_model=Notificacion)
def delete_pedido(ID: int):
    cursor = conn.cursor()
    query = "DELETE FROM notificaiones WHERE id=%s"
    notificacion = cursor.execute(query, (ID,))
    conn.commit()
    cursor.close()
    return {"mensaje": "Notificacion eliminado exitosamente"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(App, host="localhost", port=8002)