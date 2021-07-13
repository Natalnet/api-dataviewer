import React, { PureComponent } from "react";
import {
    BarChart,
    Bar,
    /* Cell,*/
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from "recharts";

// import data from '../../json/df_less_more_70.json';

const data = [

    {
        "list": "IMD0012 - 2020.6: Lista Obrigatória, Semana 1",
        "more70": 27,
        "less70": 8,
        "predict_more70": 30,
        "predict_less70": 10
    },
    {
        "list": "IMD0012 - 2020.6: Lista Preparatória, Semana 3",
        "more70": 19,
        "less70": 8,
        "predict_more70": 21,
        "predict_less70": 19
    },
    {
        "list": "ITP - Funções - Lista",
        "more70": 12,
        "less70": 5,
        "predict_more70": 10,
        "predict_less70": 5
    },
    {
        "list": "ITP - Laços",
        "more70": 24,
        "less70": 10,
        "predict_more70": 23,
        "predict_less70": 9
    },
    {
        "list": "ITP - Matriz - Lista",
        "more70": 9,
        "less70": 5,
        "predict_more70": 10,
        "predict_less70": 4
    },
    {
        "list": "ITP - Ponteiros 1 - Lista",
        "more70": 2,
        "less70": 7,
        "predict_more70": 3,
        "predict_less70": 6
    },
    {
        "list": "ITP - Recursão - Lista",
        "more70": 4,
        "less70": 5,
        "predict_more70": 5,
        "predict_less70": 4
    },
    {
        "list": "ITP - Strings - Lista",
        "more70": 16,
        "less70": 3,
        "predict_more70": 16,
        "predict_less70": 3
    }

]

export default class Example extends PureComponent {

    constructor(props) {
        super(props);
        this.state = {
            grafic: 1
        }
    }

    static jsfiddleUrl = "https://jsfiddle.net/alidingling/9hjfkp73/";

    renderGrafic(value) {
        //Verificar se a bolinha do checkbox foi marcada
        this.setState({
            grafic: value
        });
    }


    render() {
        return (
            <ResponsiveContainer width="100%" height="60%">
                <BarChart
                    data={data}
                    margin={{
                        top: 20,
                        right: 30,
                        left: 20,
                        bottom: 0,
                    }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="list" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="more70" stackId="a" fill="#82ca9d" name="Bom Desempenho" />
                    <Bar dataKey="less70" stackId="b" fill="#F08080" name="Baixo Desempenho" />
                    <Bar dataKey="predict_more70" stackId="a" fill="#2E8B57" name="Predição Bom D." />
                    <Bar dataKey="predict_less70" stackId="b" fill="#CD5C5C" name="Predição Baixo D." />
                </BarChart>
            </ResponsiveContainer>
        );
    }
}
