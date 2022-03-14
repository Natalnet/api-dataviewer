import React, { useEffect, useState } from 'react';
import { useHistory, useLocation } from 'react-router-dom';
import {
  Container,
  Typography,
  makeStyles,
  List,
  ListItem,
  Link,
  Button
} from '@material-ui/core'
import api from '../../utils/api';

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(20),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    backgroundColor: theme.palette.background.paper,
    borderRadius: '5%'
  },
  list: {
    width: '100%',
    maxWidth: 360,
  },
  text: {
    margin: theme.spacing(4, 0, 2),
    width: '100%',
    textAlign: 'center'
  },
  link: {
    color: '#495057',
  }
}));

export default function App(props) {

  const [turmas, setTurmas] = useState([]);

  useEffect(() => {
    fetchData();
  }, [])

  const fetchData = async () => {

    // Recuperar os dados da sessão    
    const user = JSON.parse(localStorage.getItem("user"));

    // Abrir umar requisição do axios para pegar as turmas do professor
    const response = await api.get(`classes/${user._id}`, {
      headers: {
        "authorization": `Bearer ${user.token}`
      }
    });

    // Mudar estado do componente
    setTurmas(response.data);
    
  }

  return (
    <div>
      <Container>
        Minhas Turmas
        {
          turmas.length > 0 
          ? <p>Turmas</p>
          // Retorna 400 se não houver nenhuma turma
          : <p>Nenhuma turma</p>
        }
      </Container>
    </div >
  );
}
