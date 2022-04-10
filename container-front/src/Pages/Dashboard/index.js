import React, { useState } from 'react';
/* Components general */
import { Card } from '../../components/BigCard/BigCard';
import ViewChart from '../../components/ViewChart/index';
import Students from "../../components/Students";
import { Box, Container, makeStyles } from '@material-ui/core'
import { useLocation } from 'react-router-dom';

const useStyles = makeStyles({
  container: {
    margin: '0 auto',
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
  },
});
/* Aqui é a classe que gerencia os json's e apresenta-os na tela como gráficos.
   Possuem mais 2 subclasses, ViewChart que é relacionado aos gráficos de turma
   e Students para os gráficos por aluno. */
export default function Dashboard(props) {
  const classes = useStyles();
  const location = useLocation();
  const { graphs } = location.state;
  const [option, setOption] = useState(1);
  const [option2, setOption2] = useState(1);
  const firstOption = "Turma";
  const secondOption = "Alunos";
  

  //Função retorna o tipo de opção dos botões entre turma e alunos para transição de tela
  //Para o gráfico de listas
  function handleClick(option) {
    if (option === firstOption)
      setOption(1);
    else
      setOption(2);
  }
  //Função retorna o tipo de opção dos botões entre turma e alunos para transição de tela
  //Para o gráfico de provas
  function handleClickSecondCard(option) {
    if (option === firstOption)
      setOption2(1);
    else
      setOption2(2);
  }
  return (
    <Container className = {classes.container} >
      <Card title="Desempenho nas listas"
        firstOption={option === 1 ? <Box fontWeight="fontWeightBold">{firstOption}</Box> : firstOption}
        secondOption={option === 2 ? <Box fontWeight="fontWeightBold">{secondOption}</Box> : secondOption}
        handleClick={handleClick}>
        {option === 1 ?
          <ViewChart moreLess={graphs.GENL} dataKeyX={"shortTitle"}
            performance={graphs.GTAL} byDifficulty={graphs.GTDL} />
          :
          <Students mediaList={graphs.media_GTNL} dataKeyX={"shortTitle"}
            dataKeyBar={"medialist"} name={"Média da lista"}
            performance={graphs.GTNL} bySubject={graphs.GEAL} byDifficulty={graphs.GEDL}
            type={"lista"} students={graphs.media_GEAL} mediaDifficulty={graphs.media_GEDL}
          />}
      </Card>
       {graphs.GENP[0].test !== undefined ? 
      <Card title="Desempenho nas provas"
        firstOption={option2 === 1 ? <Box fontWeight="fontWeightBold">{firstOption}</Box> : firstOption}
        secondOption={option2 === 2 ? <Box fontWeight="fontWeightBold">{secondOption}</Box> : secondOption}
        handleClick={handleClickSecondCard}>
        {option2 === 1 ?
          <ViewChart moreLess={graphs.GENP} dataKeyX={"test"}
            performance={graphs.GTAP} byDifficulty={graphs.GTDP} />
          :
          <Students mediaList={graphs.media_GTNP} dataKeyX={"test"} dataKeyBar={"mediatest"} name={"Média do teste"}
            performance={graphs.GTNP} bySubject={graphs.GEAP} byDifficulty={graphs.GEDP}
            type={"prova"} students={graphs.media_GEAP} mediaDifficulty={graphs.media_GEDP}
          />}
      </Card>
       : ''}
    </Container>
  );
}