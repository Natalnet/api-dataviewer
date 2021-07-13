import React, { useContext } from 'react';
import { Route, Redirect } from 'react-router-dom';
import StoreContext from '../../Store/Context';

export default function RoutesPrivate ({ component: Component, ...rest}) {
  const { token } = useContext(StoreContext);
  
  /* Caso o token tenha sido definido, o usuário é redirecionado para a página
    que ele quer, do contrário, ele é redirecionado para a página de login */
  return (
    <Route
      {...rest}
      render={() => token
        ? <Component {...rest} />
        : <Redirect to="/login" />
      }
    />
  )
}