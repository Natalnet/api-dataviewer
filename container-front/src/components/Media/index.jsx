import React from 'react';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import {
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
  Paper,
  TextField
} from '@material-ui/core';
import 'react-responsive-modal/styles.css';
import { Modal } from 'react-responsive-modal';

//Criando um componente de célula da tabela customizado
const StyledTableCell = withStyles((theme) => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
  },
}))(TableCell);
//Criando um componente de linha da tabela customizado
const StyledTableRow = withStyles((theme) => ({
  root: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover,
    },
  },
}))(TableRow);

//Passando um css usando o material-ui
const useStyles = makeStyles({
  table: {
    minWidth: 200,
  },
});

export default function App() {
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);
  const [show, setShow] = React.useState(false);
  const [type, setType] = React.useState('');
  const [proporcaoLista, setProporcaoLista] = React.useState(50);
  const [proporcaoProva, setProporcaoProva] = React.useState(50);

  //Passando uma edição da tabela que irá se comunicar com o back end no futuro
  function editData(type) {
    setType(type);
    setOpen(true);
  }
  //Mudar o valor da proporção da média que será definido pelo professor
  function handleChange(e) {
    if (type === 'Lista') {
      setProporcaoLista(e.target.value);
    } else {
      setProporcaoProva(e.target.value);
    }
  }
  //Passando as alterações para o back end
  function handleClick(e) {
    if (e.key === 'Enter' || e.key === undefined) {
      if (type === 'Lista') {
        console.log("{\n type: '" + type + "'\n proporcao: " + proporcaoLista + "\n}");
      } else {
        console.log("{\n type: '" + type + "'\n proporcao: " + proporcaoProva + "\n}");
      }
      setType('');
      setOpen(false);
    }
  }
  //Mostrar ou não a tabela
  function showContent() {
    if (show)
      setShow(false);
    else
      setShow(true);
  }
  //Fechar o modal
  function handleClose() {
    setOpen(false);
  }

  return (
    <>
      <Button onClick={showContent} >{show ? 'Minimizar' : 'Ver proporção das médias'}</Button>
      {show ?
        <TableContainer component={Paper}>
          <Table className={classes.table} aria-label="customized table">
            <TableHead>
              <TableRow>
                <StyledTableCell>Tipo</StyledTableCell>
                <StyledTableCell align="right">Proporção equivalente a média total %</StyledTableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              <StyledTableRow >
                <StyledTableCell component="th" scope="row">
                  Lista
              </StyledTableCell>
                <StyledTableCell id="number" align="right">
                  <Tooltip disableFocusListener disableTouchListener title="Edit">
                    <Button onClick={() => editData('Lista')}>{proporcaoLista}</Button>
                  </Tooltip>
                </StyledTableCell>
              </StyledTableRow>
              <StyledTableRow >
                <StyledTableCell component="th" scope="row">
                  Prova
              </StyledTableCell>
                <StyledTableCell align="right">
                  <Tooltip disableFocusListener disableTouchListener title="Edit">
                    <Button onClick={() => editData('Prova')}>{proporcaoProva}</Button>
                  </Tooltip>
                </StyledTableCell>
              </StyledTableRow>

            </TableBody>
          </Table>
        </TableContainer>
        : ''}
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="simple-modal-title"
        aria-describedby="simple-modal-description"
      >
        <h2>{type}</h2>
        <TextField
          id="standard-number"
          label="Number"
          type="number"
          InputLabelProps={{
            shrink: true,
          }}
          onChange={handleChange}
          onKeyPress={handleClick}
        />
        <Button onClick={handleClick}>Save</Button>
      </Modal>
    </>
  );
}
