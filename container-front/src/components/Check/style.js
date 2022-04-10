import styled from 'styled-components';

export const Check = styled.div`
    background: ${props => props.state ? "#D6D9DE" : "FFFFFF" };
    border: solid 1px gray;
    border-radius: 50%;
    width: 2.5vh;
    height: 2.5vh;
`;