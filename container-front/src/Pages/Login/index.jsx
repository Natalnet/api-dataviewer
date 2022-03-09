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
  const [user, setUser] = useState({});

  //Do react-router-dom, utilizado para navegar entre as telas.
  const history = useHistory();

  //Para definir o token está sendo chamado essa variável.
  const { setToken } = useContext(StoreContext);

  const [error, setError] = useState();

  // Animação do spinner
  const [loading, setLoading] = useState(false);

  // Pega ID e token dos cookies
  const id_teacher = Cookies.get("APINJS_UID");
  const token = Cookies.get("APINJS_AUTH");

  // Recebe dados do professor do GET users/:id
  async function fetchData() {

    // Recupera dados do professor
    try {

      if (!id_teacher){
        window.location.href = "http://localhost:3333";
        return
      }

      // Abrir requisição
      const response = await api.get(`users/${id_teacher}`, {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      });

      // Pôr dados no estado do componente
      setUser(response.data);

      // Colocar response.data na sessão do React
<<<<<<< HEAD
      // Redirecionar o usuario para o dashboard
      
=======
      console.log(response.data);

>>>>>>> b8cfe5f00c93be7ca1a26472f135fbd716347600

    } catch (e) {
      console.log(e.message);
    }

  }

  useEffect(() => {

    // Abrir animação do spinner 
    setLoading(true);

    // Chamar requisição
    fetchData();

    // Fechar spinner 
    setLoading(false);

  }, []);

  return (
    <Container component="main" maxWidth="xs" >
      <div className={classes.paper}>
        <div className={classes.text} >
          {user._id ?
            <Typography component="h3">
              Olá, prof. {user.name}
            </Typography>
            :
            <img src={spinnerImg} alt="Loading" style={{ width: 250 }}></img>
          }
        </div>
      </div>
    </Container>
  );
}