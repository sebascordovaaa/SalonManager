from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import Optional, List
import app.crud as crud
import re


app = FastAPI(title="SalonManager")

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
    id: int
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
    pass

# Modelo para actualizar cliente (sin ID)
class ClientesUpdate(ClientesBase):
    pass

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
            id=row["id_cliente"],
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

