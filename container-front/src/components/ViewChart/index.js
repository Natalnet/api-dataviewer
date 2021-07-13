import React, { useState } from 'react';

import MenuChart from '../MenuChart/index';

//Charts
import Grafic from '../Grafic';
import Chart4 from '../Chart_04/index';

export default function App({moreLess, dataKeyX, performance, byDifficulty}) {
    const [chart, setChart] = useState('Lista');
    //Retorna qual o tipo de gráfico irá mostrar na tela
    function viewChart(value) {
        setChart(value);
    }
    return (
        <>
            <MenuChart viewChart={viewChart} name1={'Lista'} name2={'Assunto'} name3={'Dificuldade'} name4={'Prediction'}/>

            {chart === 'Lista' ?
                <Grafic data={moreLess} dataKeyX={dataKeyX}
                    dataKeyBar0={'more'} fill0={'#82ca9d'} formatter={'list'}
                    nameBar0={'Bom Desempenho'} dataKeyBar1={'less'}
                    fill1={'#F08080'} nameBar1={'Baixo Desempenho'} 
                    dataKeyBar2={'missing'} fill2={'#808080'} nameBar2={'Faltosos'} />


                : chart === 'Assunto' ?

                    <Grafic data={performance} dataKeyX={'subject'}
                        dataKeyBar0={"more"} fill0={'#82ca9d'} formatter={'subject'}
                        nameBar0={'Alto Rendimento'} dataKeyBar1={'less'}
                        fill1={'#F08080'} nameBar1={'Baixo Rendimento'}
                        dataKeyBar2={'missing'} fill2={'#808080'} nameBar2={'Faltosos'} />
                    : chart === 'Dificuldade' ?

                        <Grafic data={byDifficulty} dataKeyX={'difficulty'}
                            dataKeyBar0={'more'} fill0={'#82ca9d'} formatter={'difficulty'}
                            nameBar0={'Acima da média'} dataKeyBar1={'less'}
                            fill1={'#F08080'} nameBar1={'Abaixo da média'}
                            dataKeyBar2={'missing'} fill2={'#808080'} nameBar2={'Faltosos'} />


                        :
                        <Chart4 />
            }
        </>
    );
}