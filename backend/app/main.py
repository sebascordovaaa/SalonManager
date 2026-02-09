from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import Optional, List
import app.crud as crud
import re


app = FastAPI(title="SalonManager")

# Configurar CORS
origins = [
    "http://localhost:5173",  # tu frontend
    "http://127.0.0.1:5173",  # también se puede usar la IP
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # permite estos orígenes
    allow_credentials=True,
    allow_methods=["*"],         # permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],         # permite cualquier encabezado
)
# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Motor de plantillas
templates = Jinja2Templates(directory="app/templates/pages")


# Importar funciones
from app.crud import(
    fetch_all_clientes,
    delete_cliente

)
# Modelo base para cliente (campos comunes, sin ID)
class ClientesBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None    
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None

# Modelo para lectura de BD (sin validaciones estrictas, acepta datos históricos)
class ClientesDB(BaseModel):
    id_cliente: int
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    fecha_registro: Optional[datetime] = None

# Modelo para crear cliente (sin ID)
class ClientesCreate(ClientesBase):
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    fecha_registro: Optional[datetime] = None


# Modelo para actualizar cliente (sin ID)
class ClientesUpdate(ClientesBase):
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    fecha_registro: Optional[datetime] = None
    

# Modelo completo de Cliente (con ID y validaciones)
class Clientes(ClientesBase):
    id: int

def map_rows_to_clientes(rows: List[dict]) -> List[ClientesDB]:
    """
    Convierte las filas del SELECT * FROM clientes (dict) 
    en objetos ClienteDB (sin validaciones estrictas para datos existentes).
    """
    return [
        ClientesDB(
            id_cliente=row["id_cliente"],
            nombre=row["nombre"],
            email=row["email"],
            telefono=row.get("telefono"),
            direccion=row.get("direccion"),
            ciudad=row.get("ciudad"),
            estado=row.get("estado"),
            codigo_postal=row.get("codigo_postal"),
            fecha_nacimiento=row.get("fecha_nacimiento"),
            fecha_registro=row.get("fecha_registro")
        )
        for row in rows
    ]




# --- GET principal ---

@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):

    rows = fetch_all_clientes()
    
    clientes = map_rows_to_clientes(rows)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "clientes": clientes
        }
    )

# ========================= CLIENTES =========================
# GET todos los clientes
@app.get("/clientes", response_model=List[ClientesDB])
def listar_clientes():
    rows = crud.fetch_all_clientes()
    return map_rows_to_clientes(rows)

# GET cliente por ID
@app.get("/clientes/{cliente_id}", response_model=ClientesDB)
def obtener_cliente(cliente_id: int):
    cliente = crud.fetch_cliente_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return ClientesDB(
        id_cliente=cliente["id_cliente"],
        nombre=cliente["nombre"],
        telefono=cliente.get("telefono"),
        email=cliente.get("email"),
        direccion=cliente.get("direccion"),
        ciudad=cliente.get("ciudad"),
        estado=cliente.get("estado"),
        codigo_postal=cliente.get("codigo_postal"),
        fecha_nacimiento=cliente.get("fecha_nacimiento"),
        fecha_registro=cliente.get("fecha_registro")
    )


# ========================= CREAR CLIENTE =========================
@app.get("/crear_clientes", response_class=HTMLResponse)
def form_nuevo_cliente(request: Request):
    return templates.TemplateResponse("crear_clientes.html", {"request": request})


@app.post("/crear_clientes")
def crear_cliente(
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: Optional[str] = Form(None),
    direccion: Optional[str] = Form(None),
    ciudad: Optional[str] = Form(None),
    estado: Optional[str] = Form(None),
    codigo_postal: Optional[str] = Form(None),
    fecha_nacimiento: Optional[datetime] = Form(None)
):
    crud.insert_cliente(nombre, telefono, email, direccion, ciudad, estado, codigo_postal, fecha_nacimiento)
    return RedirectResponse(url="/", status_code=303)


# API para crear cliente
@app.post("/api/crear_clientes")
def crear_cliente(cliente: ClientesCreate):
    # Llama a tu función de inserción de la base de datos
    crud.insert_cliente(
        cliente.nombre,
        cliente.telefono,
        cliente.email,
        cliente.direccion,
        cliente.ciudad,
        cliente.estado,
        cliente.codigo_postal,
        cliente.fecha_nacimiento
    )
    return {"message": "Cliente creado correctamente", "cliente": cliente}

# ========================= EDITAR CLIENTE =========================

@app.get("/editar_clientes/{cliente_id}", response_class=HTMLResponse)
def form_editar_cliente(request: Request, cliente_id: int):
    cliente = crud.fetch_cliente_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return templates.TemplateResponse("editar_clientes.html", {"request": request, "cliente": cliente})


@app.post("/editar_clientes/{cliente_id}")
def editar_cliente(
    cliente_id: int,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: Optional[str] = Form(None),
    direccion: Optional[str] = Form(None),
    ciudad: Optional[str] = Form(None),
    estado: Optional[str] = Form(None),
    codigo_postal: Optional[str] = Form(None),
    fecha_nacimiento: Optional[datetime] = Form(None)
):
    crud.update_cliente(cliente_id, nombre, email, telefono, direccion, ciudad, estado, codigo_postal, fecha_nacimiento)
    return RedirectResponse(url="/", status_code=303)

# Endpoint API para editar clientes
@app.put("/api/editar_clientes/{cliente_id}")
def editar_cliente(cliente_id: int, cliente: ClientesUpdate):
    # Llama a tu función de actualización existente
    crud.update_cliente(
        cliente_id,
        cliente.nombre,
        cliente.email,
        cliente.telefono,
        cliente.direccion,
        cliente.ciudad,
        cliente.estado,
        cliente.codigo_postal,
        cliente.fecha_nacimiento
    )
    return {"message": "Cliente actualizado correctamente", "cliente": cliente}


# ========================= ELIMINAR CLIENTE =========================
@app.get("/clientes/eliminar/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    """
    Endpoint para eliminar un cliente por su ID desde HTML.
    Redirige luego a la lista de clientes.
    """
    eliminado = crud.delete_cliente(cliente_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return RedirectResponse(url="/", status_code=303)


@app.delete("/api/eliminar_cliente/{cliente_id}")
def eliminar_cliente_api(cliente_id: int):
    success = crud.delete_cliente(cliente_id) 
    if not success:
        raise HTTPException(status_code=404, detail=f"Cliente con id {cliente_id} no encontrado")
    return {"message": f"Cliente con id {cliente_id} eliminado correctamente"}

