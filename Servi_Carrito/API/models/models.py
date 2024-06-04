from pydantic import BaseModel

class Carrito(BaseModel):
    id : int
    Codigo_Usuario : str
    Codigo_Producto : str
    Nombre : str
    Precio : str
    Imagen : str
    Total : str