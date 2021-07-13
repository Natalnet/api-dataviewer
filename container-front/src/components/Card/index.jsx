import React from "react";
import styled from "styled-components";

const Card = styled.div`
  width: 16em;
  margin-top: 5vh;
  min-width: 16em;
  background: #fff;
  height: 18em;
  border-radius: 1em;
  overflow: hidden;
`;

export const HeaderCard = styled.div`
  background: rgba(154, 160, 172, 0.4);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1vh;
`;

export const TitleCard = styled.div`
  font-size: 0.9em;
  font-weight: bold;
  padding: 2vh;
  margin: 0 auto;
`;

export const Options = styled.div`
  background: rgba(154, 160, 172, 0.4);
  padding: 0.5vh;
  border-radius: 20px;
  display: flex;
  align-items: center;
  margin: 0 auto;
`;

export const Option = styled.div`
  font-size: 0.9em;
  cursor: pointer;
  margin: 0 1vh;
`;

export const Line = styled.div`
  width: 1px;
  background: #fff;
  height: 3vh;
`;

const CardApp = (props) => {
  const firstOption = props.firstOption;
  const secondOption = props.secondOption;
  return (
    <Card>
      <HeaderCard>
        <TitleCard>{props.title}</TitleCard>
        {firstOption ? (
          <Options>
            {/*Estou executando a função passando o parâmetro desejado */}
            <Option onClick={() => props.handleClick(firstOption)}>
              {firstOption}
            </Option>
            <Line />
            <Option onClick={() => props.handleClick(secondOption)}>
              {secondOption}
            </Option>
          </Options>
        ) : (
          ""
        )}
      </HeaderCard>
    </Card>
  );
};
export default CardApp;