from fastapi import FastAPI, HTTPException, Query, Depends, Response
from pydantic import BaseModel
from models.models import Usuario, User
from Config.config import conn, db_config

App = FastAPI()

Usuarios = []

@App.get('/')
def index():
   return {"message": "Welcome CRUD with FastAPI Servicio Autentificacion"}

@App.get('/Lista-usuarios')
def Usuarios():
    cursor = conn.cursor()
    query = "SELECT * FROM usuarios"
    cursor.execute(query)
    usuarios = cursor.fetchall()
    cursor.close()
    return usuarios

@App.get('/Usuarios/{ID}', response_model=Usuario)
def read_Usuarios(ID: str):
    cursor = conn.cursor()
    query = "SELECT * FROM usuarios WHERE Identificacion=%s"
    cursor.execute(query,(ID,))
    usuarios = cursor.fetchone()
    cursor.close()
    if usuarios is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
            "id" : usuarios[0],
            "Nombre" : usuarios[1],
            "Correo" : usuarios[2],
            "Pasword" : usuarios[3],
            "Identificacion" : usuarios[4],
            "Direccion" : usuarios[5],
            "Rol" : usuarios[6],
        }

@App.post("/Login/")
def Login(user : User):
    Correo = user.Correo
    Pasword = user.Pasword

    cursor = conn.cursor()
    query = "SELECT * FROM usuarios WHERE Correo=%s"
    cursor.execute(query, (Correo,))
    usuario = cursor.fetchone()
    
    if usuario:
        stored_password = usuario[3]
        if Pasword == stored_password:
            cursor.close()
            return {
                "mensaje": "Éxito",
                "id" : usuario[0],
                "Nombre" : usuario[1],
                "Correo" : usuario[2],
                "Pasword" : usuario[3],
                "Identificacion" : usuario[4],
                "Direccion" : usuario[5],
                "Rol" : usuario[6],
            }
        else:
            cursor.close()
            raise HTTPException(status_code=400, detail="Correo ó Contraseña incorrecta")
    else:
        cursor.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")



@App.post('/create-Usuarios/', response_model=Usuario)
def create_Usuarios(usuarios : Usuario):
    cursor = conn.cursor()
    query = "INSERT INTO usuarios (Nombre, Correo, Pasword, Identificacion, Direccion, Rol) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (usuarios.Nombre, usuarios.Correo, usuarios.Pasword, usuarios.Identificacion, usuarios.Direccion, usuarios.Rol))
    conn.commit()
    usuarios.id = cursor.lastrowid
    cursor.close()
    return usuarios

@App.put('/update-Usuarios/{ID}', response_model=Usuario)
def update_Usuarios(ID: str, usuarios: Usuario):
    cursor = conn.cursor()
    query = "UPDATE usuarios SET Nombre=%s, Correo=%s, Pasword=%s, Identificacion=%s, Direccion=%s, Rol=%s WHERE Identificacion=%s"
    cursor.execute(query, (usuarios.Nombre, usuarios.Correo, usuarios.Pasword, usuarios.Identificacion, usuarios.Direccion, usuarios.Rol, ID))
    conn.commit()
    cursor.close()
    usuarios.id = ID
    return usuarios

@App.delete('/delete-usuarios/{ID}', response_model=Usuario)
def delete_usuarios(ID: str):
    cursor = conn.cursor()
    query = "DELETE FROM usuarios WHERE Identificacion=%s"
    usuarios = cursor.execute(query, (ID,))
    conn.commit()
    cursor.close()
    return "message Usuario removed"

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(App, host="localhost", port=8000)