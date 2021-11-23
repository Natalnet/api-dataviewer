import axios from 'axios';

/* Buscando dados de uma api remota com o endereço fixo.
   Axios é uma biblioteca que lida com aplicações rest-api no react
   facilita nossa vida, uma vez que não necessitamos definir um cabeçalho
   ou o corpo da requisição. */
const api = axios.create({
  baseURL: "http://localhost:5000/"
});

export default api;