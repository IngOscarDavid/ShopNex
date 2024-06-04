from pydantic import BaseModel

class Usuario(BaseModel):
    id : int
    Nombre : str
    Correo : str
    Pasword : str
    Identificacion : str
    Direccion : str
    Rol: int

class User(BaseModel):
    Correo : str
    Pasword : str