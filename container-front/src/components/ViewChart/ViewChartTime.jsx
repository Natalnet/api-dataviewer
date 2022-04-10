import React, { useState } from 'react';

import MenuChart from '../MenuChart/index';
import Lists from '../Lists';
import Grafic from '../Lists/Mean';
import Chart4 from '../Chart_04/index';

/* Essa classe é a que mostra os dados gerais do tempo em relação
   a todos os alunos da turma. Atualmente só tem o tempo das listas */
export default function App({ dataQuestion, dataSubmissions, dataSubject, dataDifficulty }) {
  //Variável de escolha do tipo de mostragem, por lista, por assunto e dificuldade
  const [chart, setChart] = useState('Lista');
  //Essa função retorna qual o tipo de gráfico que irá mostrar na tela
  function viewChart(value) {
    setChart(value);
  }
  return (
    <>
      <MenuChart viewChart={viewChart} name1={'Lista'}
        name2={'Assunto'} name3={'Dificuldade'} name4={'Prediction'} />

      {chart === 'Lista' ?
        <Lists dataQuestion={dataQuestion} dataSubmissions={dataSubmissions} />
        : chart === 'Assunto' ?
          <Grafic dataQuestion={dataSubject} />
          : chart === 'Dificuldade' ?
            <Grafic dataQuestion={dataDifficulty} />
            :
            <Chart4 />
      }
    </>
  );
}