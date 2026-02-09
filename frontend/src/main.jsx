import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Home.jsx";
import CrearCliente from "./CrearCliente.jsx";
import EditarCliente from "./EditarClientes.jsx";
import "bootstrap/dist/css/bootstrap.min.css";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/crear_clientes" element={<CrearCliente />} />
        <Route path="/editar_clientes/:id" element={<EditarCliente />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
