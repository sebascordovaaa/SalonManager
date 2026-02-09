import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CrearCliente() {
  const [form, setForm] = useState({
    nombre: "",
    email: "",
    telefono: "",
    direccion: "",
    ciudad: "",
    estado: "",
    codigo_postal: "",
    fecha_nacimiento: "",
  });
  const navigate = useNavigate();
  const API_URL = "http://127.0.0.1:8000";

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const res = await fetch(`${API_URL}/api/crear_clientes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error("Error al crear cliente");
      navigate("/");
    } catch (err) {
      console.error(err);
      alert("No se pudo crear el cliente");
    }
  }

  return (
    <div className="container my-5">
      <h2>Agregar Nuevo Cliente</h2>
      <div className="card p-4 mt-3">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Nombre</label>
            <input type="text" name="nombre" className="form-control" onChange={handleChange} required />
          </div>
          <div className="mb-3">
            <label className="form-label">Correo Electrónico</label>
            <input type="email" name="email" className="form-control" onChange={handleChange} required />
          </div>
          <div className="mb-3">
            <label className="form-label">Teléfono</label>
            <input type="text" name="telefono" className="form-control" onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Dirección</label>
            <input type="text" name="direccion" className="form-control" onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Ciudad</label>
            <input type="text" name="ciudad" className="form-control" onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Estado</label>
            <input type="text" name="estado" className="form-control" onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Código Postal</label>
            <input type="text" name="codigo_postal" className="form-control" onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Fecha de Nacimiento</label>
            <input type="date" name="fecha_nacimiento" className="form-control" onChange={handleChange} />
          </div>
          <div className="d-flex justify-content-between">
            <button type="button" onClick={() => navigate("/")} className="btn btn-secondary">Cancelar</button>
            <button type="submit" className="btn btn-primary">Agregar Cliente</button>
          </div>
        </form>
      </div>
    </div>
  );
}
