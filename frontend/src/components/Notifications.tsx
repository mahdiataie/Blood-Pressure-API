import { FC } from "react";
import WarningItem, { IWarningItem } from "./WarningItem";
import { styled } from "styled-components";
import { Card as AntdCard } from "antd";

const Card = styled(AntdCard)`
  width: 100%;
  overflow: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem 0;
  position: relative;
  border: 1px solid #d4d2d288;
  max-height: calc(100vh - 64px);
  min-width: 15rem;
  grid-area: c;
`;

const Container = styled.div`
  overflow: auto;
  display: flex;
  flex-direction: column;
  padding: 0 1rem;
  gap: 1rem;
  min-width: 15rem;
`;
const Header = styled.div`
  display: flex;
  padding-left: 1rem;
  justify-content: space-between;
`;

interface NotificationsProps {
  props?: IWarningItem[];
}
const Notifications: FC<NotificationsProps> = ({ props }) => {
  return (
    <Card>
      <Header>
        <h2>Warnings List</h2>
      </Header>
      <Container>
        {props &&
          props.map((warning, index) => (
            <WarningItem key={index} warning={warning as IWarningItem} />
          ))}
      </Container>
    </Card>
  );
};

export default Notifications;
