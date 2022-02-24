import React, { useState, useEffect, useContext } from 'react';
import { useHistory } from 'react-router-dom';
import api from '../../utils/api';
import StoreContext from '../../components/Store/Context';
import {
  Container,
  Typography,
  Link,
  List,
  ListItem,
  makeStyles,
} from '@material-ui/core';
import { FilterButton, FilterInput, FilterSpace } from '../../components/Students/style';
import Error from '../../components/Error';
import spinnerImg from '../../utils/spinner.svg';

import Cookies from "js-cookie";

/* Esta classe é a primeira tela para visualização do front-end. É preciso definir um token que 
   aqui está sendo definido como o id do professor escolhido.
   Se não houver token, ele vai ser sempre redirecionado para cá. */
const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(24),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    backgroundColor: theme.palette.background.paper,
    borderRadius: '2%'
  },
  form: {
    width: '90%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
    backgroundColor: '#467fcf',
    width: '100%'
  },
  text: {
    marginTop: theme.spacing(5),
    width: '100%',
    textAlign: 'center'
  },
  link: {
    color: '#495057',
  }
}));

export default function App() {

  //Para utilizar o makeStyles do material-ui é necessário esta variável
  const classes = useStyles();

  //Esta variável está sendo utilizada para guardar todos os dados da requisição
  const [user, setUser] = useState({
    _id: "",
    name: "",
    email: ""
  });

  //Do react-router-dom, utilizado para navegar entre as telas.
  const history = useHistory();

  //Para definir o token está sendo chamado essa variável.
  const { setToken } = useContext(StoreContext);

  //Esta variável está sendo utilizada para guardar os nomes dos professores.
  const [error, setError] = useState();
  const [loading, setLoading] = useState(false);

  // Pega ID e token dos cookies
  const id_teacher = Cookies.get("APINJS_UID");
  const token = Cookies.get("APINJS_AUTH");

  // Recebe dados do professor do GET users/:id
  async function fetchData() {

    // Abrir animação do spinner 
    setLoading(true);

    // Recupera dados do professor
    try {
      const response = await api.get(`users/${id_teacher}`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      const { _id, name, email } = response.data;

      // Pôr dados no estado do componente. Desenrola ai matheus
      setUser(response.data);

    } catch (e) {
      console.log(e.message);
    }

  }

  useEffect(() => {

    // Chamar requisição
    fetchData();

    // mostrar dados do professor
    console.log(user);

    // Fechar spinner
    setLoading(false);
  }, []);

  // Coloca dados na sessão


  return (
    <Container component="main" maxWidth="xs" >
      {/*Definindo um container geral para todos os componentes
         e mostrando juntos na tela.*/}
      <div className={classes.paper}>
        <div className={classes.text} >
          <Typography component="h1" variant="h4">
            Estamos preparando tudo
          </Typography>
        </div>
        <List component="nav" className={classes.list} aria-label="Turmas">
          {loading ? <img src={spinnerImg} alt="Loading" style={{ width: 250 }}></img> : false}
        </List>
      </div>
    </Container>
  );
}