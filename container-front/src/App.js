//importações necessárias
import React from 'react';
import Routes from './routes';
import GlobalStyle from './styles/global';

function App() {
    return (
        <>
        {/*Adicionando todas as rotas disponíveis na árvore*/}
            <Routes />
        {/*Adicionando um estilo padrão para todas as telas*/}
            <GlobalStyle />
        </>
    );
}

export default App;
