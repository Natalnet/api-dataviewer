import React, { useState } from 'react';
import { FormControl, FormControlLabel, RadioGroup, Radio, Checkbox } from '@material-ui/core';
import './style.css'

export default function App(props) {
    const [selectedValue, setSelectedValue] = useState(props.name1);
    //Função que mostra a tela que foi escolhida pelo usuário
    function handleChange(event) {
        setSelectedValue(event.target.value);
        props.viewChart(event.target.value);
    }
    return (
        <>
            <FormControl component="fieldset">
                <RadioGroup row aria-label="Gráficos" value={selectedValue} name="Gráficos" onChange={handleChange}>
                    <FormControlLabel value={props.name1} control={<Radio />} label={props.name1} />
                    <FormControlLabel value={props.name2} control={<Radio />} label={props.name2} />
                    { props.name3 ?
                        <FormControlLabel value={props.name3} control={<Radio />} label={props.name3} />
                        : ''
                    }
                    {props.name4 ? 
                    <FormControlLabel className="checkbox" value={props.name4}
                        control={<Checkbox checked={selectedValue === props.name4} onChange={handleChange} name={props.name4} />}
                        label={props.name4}
                    /> : ''
                    }
                </RadioGroup>
            </FormControl>

        </>
    );
}