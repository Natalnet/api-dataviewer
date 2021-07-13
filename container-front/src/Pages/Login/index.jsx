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
  const [logins, setLogins] = useState([]);
  //Do react-router-dom, utilizado para navegar entre as telas.
  const history = useHistory();
  //Para definir o token está sendo chamado essa variável.
  const { setToken } = useContext(StoreContext);
  //Esta variável está sendo utilizada para guardar os nomes dos professores.
  const [names, setNames] = useState([]);
  const [error, setError] = useState();
  const [loading, setLoading] = useState(false);

  //Utilizando o axios para fazer a requisição, usando a url padrão definida.
  async function fetchData() {
    setLoading(true);
    await api.get("/get_classes").then(response => {
      //Guardando a resposta da requisição para utilizar posteriormente 
      setLogins(response.data);
      //Iterando sobre os id's dos professores para retirar os dados iguais, evitando duplicação.
      setNames(response.data.filter((thing, index, self) =>
        index === self.findIndex((t) => (
          t.id_teacher === thing.id_teacher
        ))));
    }).catch(response => setError(response));
    setLoading(false);
  }
  useEffect(() => {
    fetchData();
  }
    , []);
  function handleClick(id) {
    //Utilizado dos dados guardados posteriormente para salvar o token.
    //Comparando o id do professor clicado com a variável global. 
    const login = logins.filter(item => item.id_teacher !== null
      && item.id_teacher.trim() === id);
    //O resultado desse filtro é um conjunto de turmas com o mesmo professor
    if (login.length !== 0) {
      //Como preciso somente do id do professor para salvar como token, 
      //coloco o primeiro resultado
      setToken(login[0].id_teacher);
      //Passando as turmas para a próxima tela.
      return history.push("/turmas", login);
    }
  }

  function handleChange(e) {
    //Definindo uma variável de busca para facilitar o encontro do nome do professor.
    let busca = e.target.value;
    /*Caso tenha alguma coisa, ele compara os nomes como caseInsensitive. 
     *Independente se está maiusculo, passando tudo para minusculo.
     *Caso não tenha nada, retorna todos os nomes, fazendo a 
     *mesma iteração para remover duplicatas.*/
    if (busca !== '')
      setNames(names.filter(item => (item.name_teacher
        .toLowerCase().includes(busca.toLowerCase()))));
    else
      setNames(logins.filter((thing, index, self) =>
        index === self.findIndex((t) => (
          t.id_teacher === thing.id_teacher
        ))));
  }
  return (
    <Container component="main" maxWidth="xs" >
      {/*Definindo um container geral para todos os componentes
         e mostrando juntos na tela.*/}
      <div className={classes.paper}>
        <div className={classes.text} >
          <Typography component="h1" variant="h4">
            Olá, Professor(a)
          </Typography>
          <Typography component="h4" variant="h6">
            Poderia selecionar o seu nome dentre as opções abaixo?
          </Typography>
        </div>
        <FilterSpace>
          <FilterInput type="text" onChange={handleChange}
            placeholder="Digite seu nome para facilitar a busca" />
          <FilterButton className="fas fa-filter" />
        </FilterSpace>
        <List component="nav" className={classes.list} aria-label="Turmas">
          {loading ? <img src={spinnerImg} alt="Loading" style={{ width: 250 }}></img> : false}
          {error ? <Error error={error} /> : names.map(item => (
            <ListItem key={item.id_teacher}>
              <Link component="button" onClick={() => handleClick(item.id_teacher)}
                className={classes.link} >
                {item.name_teacher}
              </Link>
            </ListItem>
          )
          )}
        </List>
      </div>
    </Container>
  );
}