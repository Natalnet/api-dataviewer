import React, { useState, useEffect } from 'react';
import { FormControl, InputLabel, MenuItem, Select, makeStyles } from '@material-ui/core';
import Grafic from '../Grafic/TimeGrafic';

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 300,
  },
  center: {
    display: "flex",
    justifyContent: "center",
  },
}));

export default function App({ dataQuestion }) {
  const classes = useStyles();
  const [lists, setLists] = useState([]);
  const [list, setList] = useState('');

  useEffect(() => {
    if (dataQuestion[0].subject) {
      setLists(dataQuestion.filter((thing, index, self) =>
        index === self.findIndex((t) => (
          t.subject === thing.subject
        ))));
    } else if (dataQuestion[0].difficulty) {
      setLists(dataQuestion.filter((thing, index, self) =>
        index === self.findIndex((t) => (
          t.difficulty === thing.difficulty
        ))));
    }
  }, [dataQuestion])
  const handleChange = (event) => {
    setList(event.target.value);
  };
  return (
    <>
      <FormControl className={classes.formControl + " " + classes.center}>
        <InputLabel shrink id="demo-simple-select-placeholder-label-label">
          Selecione um assunto
        </InputLabel>
        <Select
          labelId="demo-simple-select-placeholder-label-label"
          id="demo-simple-select-placeholder-label"
          value={list}
          onChange={handleChange}
          displayEmpty
          className={classes.selectEmpty}
        >
          <MenuItem value="">
            {dataQuestion[0].subject ?
            <em>Todos os Assuntos</em>
            :
            <em>Todas as Dificuldades</em>
            }
          </MenuItem>
          {dataQuestion[0].subject ? lists.map(item => (
            <MenuItem key={item.subject} value={item.subject}>{item.subject}</MenuItem>
          )) :
          lists.map(item => (
            <MenuItem key={item.difficulty} value={item.difficulty}>{item.difficulty}</MenuItem>
          ))}
        </Select>
      </FormControl>
      {dataQuestion[0].subject ? 
        <Grafic data={dataQuestion} dataKeyX={"studentMaxDifferentDaysAttempts"} type={"assunto"}
        nameX={"Tempo de resolução em dias diferentes"} valueX={'Quantidade de dias'}
        dataKeyY={"studentMaxTotalTimeAttemptInSeconds"} nameY={"Tempo máximo gasto"} list={list} name={"Tempo de resolução de cada questão"} />
        :
        <Grafic data={dataQuestion} dataKeyX={"MaxDifferentDays"} type={'dificuldade'}
        nameX={"Tempo de resolução em dias diferentes"} valueX={'Quantidade de dias'}
        dataKeyY={"maxTimeConsumingInSeconds"} nameY={"Tempo máximo gasto"} list={list} name={"Tempo de resolução de cada questão"} />
      
      }
    </>
  );
}