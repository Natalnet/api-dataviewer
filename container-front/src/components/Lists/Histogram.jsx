import React, { useEffect, useState } from 'react';
import MenuChart from '../MenuChart/index';
import { FormControl, InputLabel, MenuItem, Select, makeStyles } from '@material-ui/core';
import Grafic from '../Grafic/HistogramGrafic';

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
export default function App({ dataList, dataSubject, dataDifficulty }) {
  const classes = useStyles();
  const [lists, setLists] = useState([]);
  const [list, setList] = useState('');
  const [chart, setChart] = useState('Lista');
  useEffect(() => {
    if (chart === 'Assunto') {
      setLists(dataSubject.filter((thing, index, self) =>
        index === self.findIndex((t) => (
          t.subject === thing.subject
        ))));
    } else if (chart === 'Dificuldade') {
      setLists(dataDifficulty.filter((thing, index, self) =>
        index === self.findIndex((t) => (
          t.difficulty === thing.difficulty
        ))));
    } else {
      setLists(dataList.filter((thing, index, self) =>
        index === self.findIndex((t) => (
          t.list === thing.list
        ))));
    }
  }, [dataList, dataSubject, dataDifficulty, chart])

  function viewChart(value) {
    setChart(value);
  }
  const handleChange = (event) => {
    setList(event.target.value);
  };
  return (
    <>
       <MenuChart viewChart={viewChart} name1={'Lista'}
        name2={'Assunto'} name3={'Dificuldade'} />

      <FormControl className={classes.formControl + " " + classes.center}>
        <InputLabel id="demo-simple-select-placeholder-label-label">
          Selecione uma lista
        </InputLabel>
        <Select
          labelId="demo-simple-select-placeholder-label-label"
          id="demo-simple-select-placeholder-label"
          value={list}
          onChange={handleChange}
        >
          {chart === 'Lista' ? lists.map(item => (
            <MenuItem key={"list"+item.list} value={item.list}>{item.list}</MenuItem>
            )) : chart === 'Assunto' ?
            lists.map(item => (
                <MenuItem key={"sub"+item.subject} value={item.subject}>{item.subject}</MenuItem>
                ))
                :
                lists.map(item => (
                <MenuItem key={"dif"+item.difficulty} value={item.difficulty}>{item.difficulty}</MenuItem>
              ))
          }
        </Select>
      </FormControl>
      {chart === 'Lista' ?
        <Grafic data={dataList} dataKey={"differentDaysList"} list={list} type={'lista'}/>
        : chart === 'Assunto' ?
        <Grafic data={dataSubject} dataKey={"differentDaysSubject"} type={"assunto"}
        list={list} />
        :
        <Grafic data={dataDifficulty} dataKey={"differentDaysList"} list={list} type={'dificuldade'}/>
      }
    </>
  );
}