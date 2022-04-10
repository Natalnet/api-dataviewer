import styled from 'styled-components';

export const Header = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1em;
`;

export const FilterSpace = styled.div`
    display: flex;
    width: 75%;
    justify-content: center;
    align-items: center;
`;

export const FilterInput = styled.input`
    padding: 0.5em;
    border: 1px solid #C4C4C4;
    border-radius: 7px 0px 0px 7px;
    width: 70%;
`;

export const FilterButton = styled.div`
    color: #C4C4C4;
    display: flex;
    align-items: center;
    font-size: 0.76em;
    border: solid 1px #C4C4C4;
    padding: 1em;
    :hover{
        cursor: pointer;
    }
`;

export const FilterOptions = styled.ul`
    background: #F3F3F3;
    display: flex;
    flex-direction: column;
    overflow: auto;
    height: 3.625em;
    width: 15%;
    list-style: none;
    font-size: 0.9em;
`;

export const FilterOption = styled.li`
    margin: 0.18em;
    cursor: pointer;
`;

export const Body = styled.div`
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    overflow: auto;
    height: 19em;
    max-height: 100%;
`;

export const StudentData = styled.div`
    width: 50%;
    display: flex;
    align-items: center;
    margin: 0.6em 0;
    justify-content: space-between;
    padding-right: 1.2em;
    cursor: pointer;
    &:hover {
        color: #595959;
    }
`;

export const Div = styled.div`
    display: flex;
    align-items: center;
`;

export const StudentImage = styled.div`
    width: 2.5vw;
    height: 2.5vw;
    background: #8D5555;
    border-radius: 50%;
    margin: 0px 1vh;
`;

export const Data = styled.div`
    display: flex;
    flex-direction: column;
    margin: 0px 1vh;
`;
export const Name = styled.p`
    margin: 0.2vh;
    font-size: 1em;
`;
export const Note = styled.p`
    margin: 0.2vh;
    font-size: 0.9em;
`;

export const Indicator = styled.div`
    width: 5vh;
    height: 1.8vh;
    background: ${props => props.success ? "#76DB6D" : "#DB3030"};
    border-radius: 5px;
    margin: 0px 1vh;
`;