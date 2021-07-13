import React, { useState, useEffect } from 'react';
import ClassIcon from '@material-ui/icons/Class';
import AccessTimeIcon from '@material-ui/icons/AccessTime';
import Dashboard from '../../Pages/Dashboard'
import DashboardTime from '../../Pages/Dashboard/Time'
import { Button, Container, Tabs, Tab, makeStyles } from '@material-ui/core';
import Media from '../../components/Media'
import TabPanel from './TabPanel';
import api from '../../utils/api';
import { useHistory, useLocation } from 'react-router-dom';

const useStyles = makeStyles({
  tab: {
    flexGrow: 1,
    maxWidth: 700,
  },
  container: {
    margin: '0 auto',
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
  },
});

export default function IconTabs() {
  const classes = useStyles();
  const [value, setValue] = React.useState(0);
  const [logins, setLogins] = useState([]);
  const history = useHistory();
  const location = useLocation();
  
  useEffect(() => {
    //Retorna dados da api, que nesse caso são os nomes
    //dos professores e suas respectivas turmas
    api.get("/get_classes").then(response => {
      setLogins(response.data);
    });
    //Teste para saber se existe um gráfico sendo passado para a tela
    if(location.state === undefined)
      history.push("/login");
      
    
  }, [history, location.state]);
  //Mudando no menu a tab escolhida
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };
  //Função de retorno para mudar de turma
  function handleBack() {
    const id = sessionStorage.getItem('token').replace('"', '').replace('"', '');
    const login = logins.filter(item => item.id_teacher !== null
      && item.id_teacher.trim() === id.trim());
    history.push('/turmas', login);
  }

  return (
    <>
      <div style={{ backgroundColor: 'white' }} >
        <Container className={classes.container} >
          <Button onClick={handleBack} >Retornar para selecionar turmas</Button>
          <Tabs className={classes.tab}
            value={value}
            onChange={handleChange}
            variant="fullWidth"
            indicatorColor="primary"
            textColor="primary"
            aria-label="icon tabs example"
          >
            <Tab icon={<ClassIcon />} aria-label="phone" />
            <Tab icon={<AccessTimeIcon />} aria-label="favorite" />
          </Tabs>
          <Media />
        </Container>
      </div>
      <h1 style={{display: 'flex', justifyContent: 'center', marginTop: 20}}>{location.state === undefined ? '' : location.state.name}</h1>
      <TabPanel value={value} index={0}>
        <Dashboard  />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <DashboardTime />
      </TabPanel>
    </>
  );
}