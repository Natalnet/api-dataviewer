import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  YAxis
} from 'recharts';

export default function App(props) {
  //Passando os dados para uma lista
  const [data, setData] = useState([]);
  //Filtrando esses dados para Dias correspondentes
  const dados = data.filter((thing, index, self) =>
  index === self.findIndex((t) => (
    t.differentDaysList === thing.differentDaysList
  )));

  useEffect(()=> {
    //Passando os dados para uma variável auxiliar
    let data = props.data;
    //Caso exista uma uma props.list
    if(props.list) {
      //Ele vai testar o tipo e fazer a filtragem de acordo com esse tipo
      if(props.type==="lista")
      data = data.filter(item => item.list === props.list);
      else if(props.type==="assunto")
      data = data.filter(item => item.subject === props.list);
      else if(props.type==="dificuldade")
      data = data.filter(item => item.difficulty === props.list);
      //por fim, vai passar para a variável criada fora do useEffect
      setData(data);
      //
      //let qtd = [];
      // for (let i = 0; i < dados.length; i++) {
        //   let cont = 0;
        //   for (let j = 0; j < data.length; j++) {
      //     if(data[j].differentDaysList === dados[i].differentDaysList) {
        //       cont = cont+1;
        //     }
        //   }
        //   qtd.push(dados[i].differentDaysList + ':' + cont);
        // }
    }
  }, [props.data, props.list, props.type, dados]);
  console.log(dados.length);
  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={dados}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 0,
          }}>
          <XAxis type="number" dataKey={'differentDaysList'} />
          <YAxis type="number" />
          <Tooltip />
          <Legend />
          <Bar type="number" dataKey={props.dataKey} name="Dias diferentes" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}