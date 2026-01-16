from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import Optional, List
import re


app = FastAPI(title="SalonManager")

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Motor de plantillas
templates = Jinja2Templates(directory="app/templates")


# Importar funciones
from app.crud import(
    fetch_all_clientes
)
# Modelo base para cliente (campos comunes, sin ID)
class ClientesBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None

# Modelo para lectura de BD (sin validaciones estrictas, acepta datos históricos)
class ClientesDB(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: Optional[str] = None
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
        "pages/index.html",
        {
            "request": request,
            "clientes": clientes
        }
    )

# ========================= CLIENTES =========================
@app.get("/clientes/nuevo", response_class=HTMLResponse)
def form_nuevo_cliente(request: Request):
    return templates.TemplateResponse("nuevo_cliente.html", {"request": request})

@app.post("/clientes/nuevo")
def crear_cliente(
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    telefono: Optional[str] = Form(None),
    direccion: Optional[str] = Form(None)
):
    crud.insert_cliente(nombre, apellido, email, telefono, direccion)
    return RedirectResponse(url="/clientes", status_code=303)

@app.get("/clientes/editar/{cliente_id}", response_class=HTMLResponse)
def form_editar_cliente(request: Request, cliente_id: int):
    cliente = crud.fetch_cliente_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return templates.TemplateResponse("editar_cliente.html", {"request": request, "cliente": cliente})

@app.post("/clientes/editar/{cliente_id}")
def editar_cliente(
    cliente_id: int,
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    telefono: Optional[str] = Form(None),
    direccion: Optional[str] = Form(None)
):
    crud.update_cliente(cliente_id, nombre, apellido, email, telefono, direccion)
    return RedirectResponse(url="/clientes", status_code=303)





# ========================= EMPLEADOS =========================
@app.get("/empleados/nuevo", response_class=HTMLResponse)
def form_nuevo_empleado(request: Request):
    return templates.TemplateResponse("nuevo_empleado.html", {"request": request})

@app.post("/empleados/nuevo")
def crear_empleado(
    nombre: str = Form(...),
    especialidad: str = Form(...),
    telefono: Optional[str] = Form(None),
    email: Optional[str] = Form(None)
):
    crud.insert_empleado(nombre, especialidad, telefono, email)
    return RedirectResponse(url="/empleados", status_code=303)

@app.get("/empleados/editar/{empleado_id}", response_class=HTMLResponse)
def form_editar_empleado(request: Request, empleado_id: int):
    empleado = crud.fetch_empleado_by_id(empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return templates.TemplateResponse("editar_empleado.html", {"request": request, "empleado": empleado})

@app.post("/empleados/editar/{empleado_id}")
def editar_empleado(
    empleado_id: int,
    nombre: str = Form(...),
    especialidad: str = Form(...),
    telefono: Optional[str] = Form(None),
    email: Optional[str] = Form(None)
):
    crud.update_empleado(empleado_id, nombre, especialidad, telefono, email)
    return RedirectResponse(url="/empleados", status_code=303)

# ========================= SERVICIOS =========================
@app.get("/servicios/nuevo", response_class=HTMLResponse)
def form_nuevo_servicio(request: Request):
    return templates.TemplateResponse("nuevo_servicio.html", {"request": request})

@app.post("/servicios/nuevo")
def crear_servicio(
    nombre: str = Form(...),
    precio: float = Form(...)
):
    crud.insert_servicio(nombre, precio)
    return RedirectResponse(url="/servicios", status_code=303)

@app.get("/servicios/editar/{servicio_id}", response_class=HTMLResponse)
def form_editar_servicio(request: Request, servicio_id: int):
    servicio = crud.fetch_servicio_by_id(servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return templates.TemplateResponse("editar_servicio.html", {"request": request, "servicio": servicio})

@app.post("/servicios/editar/{servicio_id}")
def editar_servicio(
    servicio_id: int,
    nombre: str = Form(...),
    precio: float = Form(...)
):
    crud.update_servicio(servicio_id, nombre, precio)
    return RedirectResponse(url="/servicios", status_code=303)

# ========================= CITAS =========================
@app.get("/citas/nuevo", response_class=HTMLResponse)
def form_nueva_cita(request: Request):
    clientes = crud.fetch_all_clientes()
    empleados = crud.fetch_all_empleados()
    servicios = crud.fetch_all_servicios()
    return templates.TemplateResponse(
        "nueva_cita.html",
        {"request": request, "clientes": clientes, "empleados": empleados, "servicios": servicios}
    )

@app.post("/citas/nuevo")
def crear_cita(
    id_cliente: int = Form(...),
    id_empleado: int = Form(...),
    id_servicio: int = Form(...),
    fecha: str = Form(...)
):
    crud.insert_cita(id_cliente, id_empleado, id_servicio, fecha)
    return RedirectResponse(url="/citas", status_code=303)

@app.get("/citas/editar/{cita_id}", response_class=HTMLResponse)
def form_editar_cita(request: Request, cita_id: int):
    cita = crud.fetch_cita_by_id(cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    clientes = crud.fetch_all_clientes()
    empleados = crud.fetch_all_empleados()
    servicios = crud.fetch_all_servicios()
    return templates.TemplateResponse(
        "editar_cita.html",
        {"request": request, "cita": cita, "clientes": clientes, "empleados": empleados, "servicios": servicios}
    )

@app.post("/citas/editar/{cita_id}")
def editar_cita(
    cita_id: int,
    id_cliente: int = Form(...),
    id_empleado: int = Form(...),
    id_servicio: int = Form(...),
    fecha: str = Form(...)
):
    crud.update_cita(cita_id, id_cliente, id_empleado, id_servicio, fecha)
    return RedirectResponse(url="/citas", status_code=303)