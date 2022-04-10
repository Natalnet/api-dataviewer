import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

//Árvore de renderização. Pegando o componente app e colocando na div html com id root
ReactDOM.render(
  <App />,
  document.getElementById('root')
);
