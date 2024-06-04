from pydantic import BaseModel

class Pedido(BaseModel):
    id : int
    Direccion : str
    Estado : str
    Ubicacion : str
    Metodo_Pago : str
    Total_Pagar : str