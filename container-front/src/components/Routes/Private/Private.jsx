import React, { useEffect, useState } from 'react';
import { Route } from 'react-router-dom';
import api from '../../../utils/api';
import Cookies from "js-cookie";

export default function RoutesPrivate({ component: Component, ...rest }) {

  const id_teacher = Cookies.get("APINJS_UID");
  const token = Cookies.get("APINJS_AUTH");
  const [userExists, setUserExists] = useState(true);

  useEffect(() => {
    fetchData();
  }, [])

  const fetchData = async () => {
    
    try {
      // Abrir requisição
      const response = await api.get(`users/${id_teacher}`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      // Recuperar dados
      const data = response.data;
  
      // Adicionar token na sessão
      data["token"] = token;
  
      setUserExists(true);
  
      // Colocar na sessão
      localStorage.setItem("user", JSON.stringify(data));

    } catch(e) {
      setUserExists(false);
    }

  }

  return (
    <Route
      {...rest}
      // Token e id_teacher válidos?
      render = {() => userExists === true
        ? <Component {...rest} /> // usuário vê o componente
        : window.location.href = "http://localhost:3333" // usuário redirecionado
      }
    />
  )
}