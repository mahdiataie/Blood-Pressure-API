import { FC, useState, useEffect } from "react";
import Notifications from "../components/Notifications";
import { Card, Button } from "antd";
import styled from "styled-components";
import warning from "./warning.png";
import { IWarningItem } from "../components/WarningItem";
import moment from "moment";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { LogoutOutlined, LoadingOutlined } from "@ant-design/icons";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import ChartComponent from "../components/ChartComponent";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);
interface INotificationProps {
  color?: string;
}
const Header = styled.div`
  position: sticky;
  left: 0;
  top: 0;
  height: 64px;
  width: 100%;
  background-color: #001529;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
`;

const NotificationBox = styled(Card)<INotificationProps>`
  height: 20rem;
  gap: 10px;
  background-color: ${(props) => props.color};
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
    rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
  position: relative;
  justify-content: center;
  font: 1.5em sans-serif;
  min-width: 21rem;
  grid-area: b;
  max-width: 30rem;
`;

const Content = styled.div`
  display: grid;
  gap: 1rem;
  grid-template-areas:
    "a b c"
    "d d c";
  padding: 1rem;
  @media (max-width: 1110px) {
    display: flex;
    flex-direction: column;
  }
`;

const LatestBox = styled(Card)`
  height: 20rem;
  gap: 10px;
  background-color: white;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
    rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
  position: relative;
  justify-content: center;
  font: 1.5em sans-serif;
  min-width: 21rem;
  grid-area: a;
  max-width: 30rem;
`;

const Dashboard: FC = () => {
  const [boxColor, setBoxColor] = useState("#AFE1AF"); // Default color
  const [warningMessage, setWarningMessage] = useState<string>(
    "Everything looks fine!"
  );
  const [measurementType, setMeasurementType] = useState<string | null>(null);
  const [lastMeasurement, setLatestMeasurement] = useState<Float32Array>();
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const navigate = useNavigate();
  const [warnings, setWarnings] = useState<IWarningItem[]>([]);
  const [chartData, setChartData] = useState([]);
  const host = window.location.hostname;

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      axios
        .get("http://127.0.0.1:8000/api/measures/latest/", {
          headers: {
            Authorization: `Token ${token}`,
            "Content-Type": "application/json",
          },
        })
        .then((response: any) => {
          // console.log('warning data', response.data)
          console.log(response.data);
          setChartData(response.data);
        })
        .catch((error) => {
          console.log(error.request.response);
        });
    }
  }, [lastMeasurement]);
  useEffect(() => {
    requestNotificationPermission();
    const token = localStorage.getItem("token"); // Token retrieved from local storage after user login
    let listOfWarnings: IWarningItem[] = [];

    if (token) {
      // Sending initial request to get list of warnings
      axios
        .get("http://127.0.0.1:8000/api/household/warnings/", {
          headers: {
            Authorization: `Token ${token}`,
            "Content-Type": "application/json",
          },
        })
        .then((response: any) => {
          listOfWarnings = response.data;
          setWarnings(response.data);
        })
        .catch((error) => {
          console.log(error.request.response);
        });

      // opening websocket connection using token
      const socket = new WebSocket(
        `ws://127.0.0.1:8000/ws/notifications/?token=${token}`
      );
      setSocket(socket);

      socket.onopen = () => {
        console.log("WebSocket connected");
      };

      socket.onmessage = (event) => {
        // event for getting new notification from websocket
        const data = JSON.parse(event.data);

        const { value, timestamp, measuretype_name } = data;

        let formattedDate = moment(timestamp).format("DD-MMM-YYYY LT");

        setMeasurementType(measuretype_name);
        setLatestMeasurement(value);
        if (data.warning_code === "YELLOW") {
          setBoxColor("#ecdd92");
          setWarningMessage(
            `This is a warning for ${measuretype_name} with Value of : ${value}.\n Time :${formattedDate}`
          );
          setWarnings([data as IWarningItem, ...listOfWarnings]);
        }
        if (data.warning_code === "RED") {
          setBoxColor("#fb9d94");
          setWarningMessage(
            `This is a critical warning for ${measuretype_name} with Value of : ${value}.\n Time :${formattedDate}`
          );
          setWarnings([data as IWarningItem, ...listOfWarnings]);
        }
        if (data.warning_code === "GREEN") {
          setBoxColor("#AFE1AF");
          setWarningMessage(`Everything looks fine!`);
        }
      };

      socket.onclose = () => {
        console.log("WebSocket closed");
      };

      // Add a beforeunload event listener to close the socket when the user leaves the page
      window.addEventListener("beforeunload", () => {
        socket.close();
        setSocket(null);
      });
    }

    // Cleanup function
    return () => {
      if (socket) {
        socket.close();
        setSocket(null); // Set the socket state to null to indicate the connection is closed
        window.removeEventListener("beforeunload", () => {});
      }
    };
  }, [localStorage]);

  useEffect(() => {
    if (warningMessage !== "Everything looks fine!") {
      showNotification(warningMessage);
    }
  }, [warningMessage]);

  const requestNotificationPermission = async () => {
    // getting users permisssion for sending notification using the browser
    if ("Notification" in window) {
      const permission = await Notification.requestPermission();
      return permission === "granted";
    }
    return false;
  };

  const showNotification = (warningMessage: string) => {
    if (Notification.permission === "granted") {
      new Notification("Blood Pressure Warning", {
        body: warningMessage,
        icon: warning,
      });
    }
  };

  const logout = () => {
    socket?.close();
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div>
      <Header>
        <Button icon={<LogoutOutlined />} onClick={logout}>
          Logout
        </Button>
      </Header>

      <Content>
        <LatestBox>
          <h3>Latest Blood Pressure:</h3>
          <br></br>
          <h3>{measurementType}</h3>
          <br></br>
          {!lastMeasurement && (
            <h4 style={{ fontFamily: "sans-serif" }}>waiting for a new data</h4>
          )}
          {!lastMeasurement && (
            <h1 style={{ fontFamily: "sans-serif", fontSize: "5rem" }}>
              <LoadingOutlined />
            </h1>
          )}
          {lastMeasurement && (
            <h1 style={{ fontFamily: "sans-serif", fontSize: "5rem" }}>
              {lastMeasurement}
            </h1>
          )}
          <br></br>
        </LatestBox>
        <NotificationBox color={boxColor}>
          <h3>REAL-TIME WARNING:</h3> <br></br>
          {warningMessage}
        </NotificationBox>
        <Notifications props={warnings} />
        <ChartComponent dataPoints={chartData} />
      </Content>
    </div>
  );
};

export default Dashboard;
