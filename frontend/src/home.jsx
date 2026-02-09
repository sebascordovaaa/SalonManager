import { useEffect, useState } from "react";
import Header from "./Header";
import Banner from "./Banner";
import ClientesTabla from "./ClientesTabla";
import Footer from "./Footer";

export default function Home() {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const API_URL = "http://127.0.0.1:8000";

  useEffect(() => {
    fetch(`${API_URL}/clientes`)
      .then(res => res.json())
      .then(data => setClientes(data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <>
      <Header />
      <div className="container my-5">
        <Banner />
        {loading ? <p>Cargando clientes...</p> : <ClientesTabla clientes={clientes} setClientes={setClientes} />}
      </div>
      <Footer />
    </>
  );
}
