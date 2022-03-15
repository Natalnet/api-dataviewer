import {
  Container
} from "@material-ui/core"
import { useEffect, useState } from "react";

import {
  useParams
} from "react-router-dom"
import api from "../../utils/api";


export default function App(props) {

  // Gráficos
  const [graphs, setGraphs] = useState([])

  // Recuperar o id da turma
  const { id_class } = useParams();

  const fetchData = async () => {

    // Recuperar os dados da sessão
    const user = JSON.parse(localStorage.getItem("user"));


    // Recuperar os gráficos dessa turma
    const response = await api.get(`graphs/${id_class}`, {
      headers: {
        "authorization": `Bearer ${user.token}`
      }
    });

    // Atualizar o estado
    setGraphs(response.data);

    console.log(response.data);
  }

  useEffect(() => {
    fetchData();
  },[])

  return (
    <Container>
      Olá, você quer ver os gráficos da Turma {id_class}
      {
        graphs.length > 0
        ? <p>Os dados podem ser vistos no console</p>
        : <p>Nenhum gráfico</p>
      }
    </Container>
  );
}