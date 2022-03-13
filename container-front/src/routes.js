import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
} from 'react-router-dom';
import StoreProvider from './components/Store/Provider';
import RoutesPrivate from './components/Routes/Private/Private';
import Home from './components/Menu';
import Turmas from './Pages/Turmas';

export default function App() {
    return (
        <Router>
            <StoreProvider>
                <Switch>
                    {/*RoutesPrivate é uma rota que está verificando se o token de acesso está disponível.
                       Caso não esteja, retorna para a rota de login. */}
                    <RoutesPrivate path="/turmas" component={Turmas} />
                    <RoutesPrivate path="/" component={Home} />
                </Switch>
            </StoreProvider>
        </Router>
    );
}
