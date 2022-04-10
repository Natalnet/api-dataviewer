import React, { useState, useEffect } from 'react';
import MenuChart from '../MenuChart/index';
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

export default function App({ dataQuestion, dataSubmissions }) {
  const classes = useStyles();
  const [lists, setLists] = useState([]);
  const [list, setList] = useState('');
  const [chart, setChart] = useState('Questão');

  useEffect(() => {
    setLists(dataQuestion.filter((thing, index, self) =>
      index === self.findIndex((t) => (
        t.list === thing.list
      ))));
  }, [dataQuestion])
  function viewChart(value) {
    setChart(value);
  }
  const handleChange = (event) => {
    setList(event.target.value);
  };
  return (
    <>
      <div className={classes.center} >
        <MenuChart viewChart={viewChart} name1={'Questão'}
          name2={'Submissão'} />
      </div>
      {chart === 'Questão' ?
        <>
          <FormControl className={classes.formControl+" "+classes.center}>
            <InputLabel shrink id="demo-simple-select-placeholder-label-label">
              Selecione uma Lista
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
                <em>Todas as Listas</em>
              </MenuItem>
              {lists.map(item => (
                <MenuItem key={item.question} value={item.list}>{item.list}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <Grafic data={dataQuestion} dataKeyX={"maxDifferentDays"} type={'lista'}
            nameX={"Tempo de resolução em dias diferentes"} valueX={'Quantidade de dias'}
            dataKeyY={"maxTime"} nameY={"Tempo máximo gasto"} list={list} name={"Tempo de resolução de cada questão"} />
        </>
        : <Grafic data={dataSubmissions} dataKeyX={"quantity"}
          nameX={"Quantidade de submissões"} valueX={'Quantidade de submissões'}
          dataKeyY={"timeInSecounds"} nameY={"Tempo máximo gasto"} name={"Quantidade de submissões e tempo gasto por questão"} />

      }
    </>
  );
}