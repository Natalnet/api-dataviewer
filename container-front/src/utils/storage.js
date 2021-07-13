import Cookie from 'js-cookie';

const storage = {};

/*Caso do navegador não tiver sessionStorage
  ele lança uma excessão */
try {
  if (!window.sessionStorage) {
    throw Error('no session storage');
  }

  /* Definindo o valor, e sua chave. No nosso caso é o token.
     Guardando o token na sessão, caso o usuário feche o navegador
     a sessão é encerrada. */
  storage.set = (key, value) => sessionStorage.setItem(key, JSON.stringify(value));
  storage.get = (key) => {
    const item = sessionStorage.getItem(key);
    try {
      return JSON.parse(item);
    } catch (e) {
      return null;
    }
  };
  //Para remover o item do navegador manualmente. Caso seja necessário.
  storage.remove = key => sessionStorage.removeItem(key);
} catch (e) {
  //definindo utilizações de cookie
  storage.set = Cookie.set;
  storage.get = Cookie.getJSON;
  storage.remove = Cookie.remove;
}

export default storage;