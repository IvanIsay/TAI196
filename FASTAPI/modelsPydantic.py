
from pydantic import BaseModel,Field, EmailStr

#modelo para validacion de datos
class modelUsuario(BaseModel):
    id:int = Field(...,gt=0, description="Id unico y solo numeros positivos")
    nombre:str = Field(..., min_length=3 ,max_length=15, description="Nombre debe contener solo letras y espacios" )
    edad:int
    correo:str

class modelAuth(BaseModel):
    correo:EmailStr
    passw:str = Field(..., min_length=8,strip_whitespace=True, description=" Contraseña minimo 8 caracteres")
