import React, { useEffect, useState } from 'react';
import { CartesianGrid, Cell, Legend, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis, ZAxis } from 'recharts';
import { scaleOrdinal } from 'd3-scale';
import { schemeCategory10 } from 'd3-scale-chromatic';

const colors = scaleOrdinal(schemeCategory10).range();

export default function App(props) {
  const [data, setData] = useState([]);
  useEffect(()=> {
    let data = props.data;
    if(props.list && !props.registration) {
      if(props.type==="lista")
      data = data.filter(item => item.list === props.list);
      else if(props.type==="assunto")
      data = data.filter(item => item.subject === props.list);
      else if(props.type==="dificuldade")
      data = data.filter(item => item.difficulty === props.list);
      setData(data);
    } else if (props.list && props.registration) {
      if(props.type==="lista")
      data = data.filter(item => item.list === props.list && item.registration===props.registration);
      else if(props.type==="assunto")
      data = data.filter(item => item.subject === props.list && item.registration===props.registration);
      else if(props.type==="dificuldade")
      data = data.filter(item => item.difficulty === props.list && item.registration===props.registration);
      setData(data);
    } else {
      setData(data);
    }
  }, [props.data, props.list, props.registration, props.type])
  return (
    <ResponsiveContainer width="100%" height={props.list === '' || props.list ? "58%" : "70%"}>
      <ScatterChart
        margin={{ top: 20, right: 20, bottom: 10, left: 50 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis type="number" dataKey={props.dataKeyX} allowDecimals={false}
        name={props.nameX}
        label={{ value: props.valueX, viewBox: { x: 240, y: props.list === '' || props.list ? 280 : 344, width: 50, height: 50 }}}/>
        <YAxis type="number" dataKey={props.dataKeyY} name={props.nameY} unit="s" 
        label={{ value: 'Tempo máximo gasto', angle: -90, viewBox: { x: 0, y: 80, width: 50, height: 50 } }}
        domain={[0, 'dataMax']} scale="linear" />
        <ZAxis type="category" dataKey="question" name="Questão" />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Legend />
        <Scatter name={props.name} data={data} fill="#8884d8">
          {
            data.map((entry, index) => <Cell key={`cell-${index}`} fill={colors[index % colors.length]}>{entry.question}</Cell>)
          }
        </Scatter>
      </ScatterChart>
    </ResponsiveContainer>
  );
}