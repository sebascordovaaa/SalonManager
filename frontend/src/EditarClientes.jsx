import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

export default function EditarCliente() {
  const { id } = useParams();
  const [cliente, setCliente] = useState(null);
  const navigate = useNavigate();
  const API_URL = "http://127.0.0.1:8000";

  useEffect(() => {
    fetch(`${API_URL}/clientes/${id}`)
      .then(res => res.json())
      .then(data => setCliente(data))
      .catch(err => console.error(err));
  }, [id]);

  function handleChange(e) {
    setCliente({ ...cliente, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const res = await fetch(`${API_URL}/api/editar_clientes/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cliente),
      });
      if (!res.ok) throw new Error("No se pudo actualizar cliente");
      navigate("/");
    } catch (err) {
      console.error(err);
      alert("No se pudo actualizar el cliente");
    }
  }

  if (!cliente) return <p>Cargando cliente...</p>;

  return (
    <div className="container my-5">
      <h2>Editar Cliente</h2>
      <div className="card p-4 mt-3">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Nombre</label>
            <input type="text" name="nombre" className="form-control" value={cliente.nombre} onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Correo Electrónico</label>
            <input type="email" name="email" className="form-control" value={cliente.email} onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Teléfono</label>
            <input type="text" name="telefono" className="form-control" value={cliente.telefono || ""} onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Dirección</label>
            <input type="text" name="direccion" className="form-control" value={cliente.direccion || ""} onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Ciudad</label>
            <input type="text" name="ciudad" className="form-control" value={cliente.ciudad || ""} onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Estado</label>
            <input type="text" name="estado" className="form-control" value={cliente.estado || ""} onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Código Postal</label>
            <input type="text" name="codigo_postal" className="form-control" value={cliente.codigo_postal || ""} onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label className="form-label">Fecha de Nacimiento</label>
            <input type="date" name="fecha_nacimiento" className="form-control" value={cliente.fecha_nacimiento?.split("T")[0] || ""} onChange={handleChange} />
          </div>
          <div className="d-flex justify-content-between">
            <button type="button" onClick={() => navigate("/")} className="btn btn-secondary">Cancelar</button>
            <button type="submit" className="btn btn-success">Guardar Cambios</button>
          </div>
        </form>
      </div>
    </div>
  );
}
