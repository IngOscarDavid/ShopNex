from pydantic import BaseModel

class Producto(BaseModel):
    id : int
    Codigo : str
    Nombre : str
    Descripcion : str
    Catalogo : str
    Precio : str
    Cantidad  : str
    Image : str
    Descuento : str