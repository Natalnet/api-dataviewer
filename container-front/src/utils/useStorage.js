import { useCallback, useState } from 'react';
import storage from './storage';

export default function useStorage(key) {
  //pegando a chave diretamente do storage
  const [state, setState] = useState(() => storage.get(key));
  //Guardando um valor no storage
  const set = useCallback(newValue => {
    storage.set(key, newValue);
    setState(newValue);
  }, [key]);
  //removendo o valor guardado
  const remove = useCallback(() => {
    storage.remove(key);
    setState(undefined);
  }, [key]);

  return [state, set, remove];
}