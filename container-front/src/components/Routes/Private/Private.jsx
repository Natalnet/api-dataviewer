import React, { useEffect, useState } from 'react';
import { Route } from 'react-router-dom';
import api from '../../../utils/api';
import Cookies from "js-cookie";
import spinnerImg from '../../../utils/spinner.svg';

export default function RoutesPrivate({ component: Component, ...rest }) {

  const id_teacher = Cookies.get("APINJS_UID");
  const token = Cookies.get("APINJS_AUTH");
  const [loading, setLoading] = useState(false);

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
  
      setLoading(true);
  
      // Colocar na sessão
      localStorage.setItem("user", JSON.stringify(data));

    } catch(e) {
      window.location.href = "http://localhost:3333"
      setLoading(false);
    }

  }

  return (
    <Route
      {...rest}
      // Token e id_teacher válidos?
      render = {() => loading === true
        ? <Component {...rest} /> // usuário vê o componente
        : <img src={spinnerImg} alt="Loading" style={{ width: 250 }}></img> 
      }
    />
  )
}