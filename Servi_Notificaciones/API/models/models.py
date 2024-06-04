from pydantic import BaseModel

class Notificacion(BaseModel):
    id : int
    Codigo_Usuario : str
    Texto : str
    Estado : str

class Not(BaseModel):
    id :int
    Estado : str
