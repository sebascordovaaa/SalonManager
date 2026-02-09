import { useNavigate } from "react-router-dom";

export default function ClientesTabla({ clientes, setClientes }) {
  const navigate = useNavigate();
  const API_URL = "http://127.0.0.1:8000";

  async function handleEliminar(id) {
    if (!window.confirm("¿Eliminar este cliente?")) return;
    try {
      const res = await fetch(`${API_URL}/api/eliminar_cliente/${id}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("No se pudo eliminar");
      // Actualizamos la lista en Home
      setClientes(clientes.filter(c => c.id_cliente !== id));
    } catch (err) {
      console.error("Error al eliminar cliente:", err);
    }
  }


  function formatDate(dateStr) {
    return dateStr ? new Date(dateStr).toLocaleDateString() : "-";
  }

  if (!clientes || clientes.length === 0) return <p>No hay clientes.</p>;

  return (
    <div className="card p-4 mb-5">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4>Clientes</h4>
        <button onClick={() => navigate("/crear_clientes")} className="btn btn-gradient">
          ➕ Añadir Cliente
        </button>
      </div>

      <div className="table-container">
        <table className="table table-hover align-middle">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Email</th>
              <th>Teléfono</th>
              <th>Dirección</th>
              <th>Ciudad</th>
              <th>Estado</th>
              <th>Código Postal</th>
              <th>Fecha de Nacimiento</th>
              <th>Registro</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {clientes.map(c => (
              <tr key={c.id_cliente}>
                <td>{c.nombre}</td>
                <td>{c.email}</td>
                <td>{c.telefono || "-"}</td>
                <td>{c.direccion || "-"}</td>
                <td>{c.ciudad || "-"}</td>
                <td>{c.estado || "-"}</td>
                <td>{c.codigo_postal || "-"}</td>
                <td>{formatDate(c.fecha_nacimiento)}</td>
                <td>{formatDate(c.fecha_registro)}</td>
                <td>
                  <button onClick={() => navigate(`/editar_clientes/${c.id_cliente}`)} className="edit-btn">✏️</button>
                  <button onClick={() => handleEliminar(c.id_cliente)} className="delete-btn">🗑</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
