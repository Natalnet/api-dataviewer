import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import './style.css';

export default function App(props) {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
          <p className="label">{`${label}`}</p> 
          <p>{`${payload[0].payload.list}`}</p>
          <p>{`${payload[0].name}: ${payload[0].value}`}</p>
          <p>{`${payload[1].name}: ${payload[1].value}`}</p>
          <p>{`${payload[2].name}: ${payload[2].value}`}</p>
        </div>
      );
    }
  
    return null;
  };

    return (
      <ResponsiveContainer width="100%" height="68%">
        <BarChart
          data={props.data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 0,
          }}

        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={props.dataKeyX} />
          <YAxis unit={props.yUnit ? props.yUnit : ''} label={{ value: 'Quantidade de alunos', angle: -90, viewBox: { x: 20, y: 100, width: 50, height: 50 } }} />
          <Tooltip content={<CustomTooltip />} />
          <Legend verticalAlign="top" />
          <Bar dataKey={props.dataKeyBar0} fill={props.fill0} name={props.nameBar0} />
          {props.dataKeyBar1 ?
            <Bar dataKey={props.dataKeyBar1} fill={props.fill1} name={props.nameBar1} /> : ''}
          {props.dataKeyBar2 ?
            <Bar dataKey={props.dataKeyBar2} fill={props.fill2} name={props.nameBar2} />
            : ''}
          {props.dataKeyBar3 ?
            <Bar dataKey={props.dataKeyBar3} fill={props.fill3} name={props.nameBar3} />
            : ''}
        </BarChart>
      </ResponsiveContainer>
    );

  }