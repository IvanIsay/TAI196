
from fastapi import FastAPI, HTTPException,Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from modelsPydantic import modelUsuario, modelAuth
from tokenGen import createToken
from middlewares import BearerJWT

app= FastAPI(
    title='Mi primer API 196',
    description='Ivan Isay Guerra Lopez',
    version= '1.0.1'
)



usuarios=[
    {"id":1, "nombre":"ivan", "edad": 37, "correo":"ivan@example.com"},
    {"id":2, "nombre":"Estrella", "edad": 21, "correo":"estrella@example.com"},
    {"id":3, "nombre":"Carlos", "edad": 21, "correo":"carlos@example.com"},
    {"id":4, "nombre":"Isacc", "edad": 21, "correo":"isacc@example.com"},
]

@app.get('/',tags=['Inicio'])
def main():
    return {'hola FastAPI':'IvanIsay'}

#endpoint para generar token
@app.post('/auth', tags=['Autentificacion'])
def login(autorizado:modelAuth):
    if autorizado.correo == 'ivan@example.com' and autorizado.passw == '123456789':
        token:str = createToken(autorizado.model_dump())
        print(token)
        return JSONResponse(content= token)
    else:
        return {"Aviso":"Usuario no Autorizado"}
    

#endpoint Consultar todos
@app.get('/usuarios', dependencies=[Depends(BearerJWT())] , response_model= List[modelUsuario], tags=['Operaciones CRUD'])
def ConsultarTodos():
    return usuarios



#endpoint Para Agregar usuarios
@app.post('/usuario/', response_model=modelUsuario ,tags=['Operaciones CRUD'])
def AgregarUsuario(usuarionuevo: modelUsuario):
    for usr in usuarios:
        if usr["id"] == usuarionuevo.id:
            raise HTTPException(status_code=400, detail="El id ya esta registrado")

    usuarios.append(usuarionuevo)
    return usuarionuevo



# Actualizar usuario (PUT)
@app.put("/usuarios/{id}", response_model=modelUsuario,tags=["Operaciones CRUD"])
def actualizar_usuario(id: int, usuario_actualizado:modelUsuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index]= usuario_actualizado.model_dump()  
            return usuarios[index]
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")


# Eliminar usuario (DELETE)
@app.delete("/usuarios/{id}", tags=["Operaciones CRUD"])
def eliminar_usuario(id: int):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {"mensaje": f"Usuario con ID {id} eliminado."}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")