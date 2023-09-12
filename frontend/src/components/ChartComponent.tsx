import { FC } from "react";
import { Line } from "react-chartjs-2";
import { styled } from "styled-components";

const Container = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-area: d;
  max-width: 60rem;
  @media (max-width: 1110px) {
    display: flex;
    flex-direction: column;
  }
`;
interface ChartComponentProps {
  dataPoints: { timestamp: string; value: string; measure_type: number }[];
}
const ChartComponent: FC<ChartComponentProps> = ({ dataPoints }) => {
  const reversedDataPoints = [...dataPoints].reverse();

  const datasetValue1 = reversedDataPoints
    .filter((dataPoint) => dataPoint.measure_type === 10)
    .map((dataPoint) => ({
      x: dataPoint.timestamp.substr(0, 10),
      y: dataPoint.value,
    }));
  const datasetValue2 = reversedDataPoints
    .filter((dataPoint) => dataPoint.measure_type === 9)
    .map((dataPoint) => ({
      x: dataPoint.timestamp.substr(0, 10),
      y: dataPoint.value,
    }));

  return (
    <Container>
      <div>
        <h2>Systolic Blood Pressure</h2>
        <Line
          data={{
            labels: [],
            datasets: [
              {
                label: "Blood Pressure",
                data: datasetValue1,
                borderColor: "rgba(75,192,192,1)",
              },
            ],
          }}
        />
      </div>
      <div>
        <h2>Diastolic Blood Pressure</h2>
        <Line
          data={{
            labels: [],
            datasets: [
              {
                label: "Blood Pressure",
                data: datasetValue2,
                borderColor: "rgba(192,75,192,1)",
              },
            ],
          }}
        />
      </div>
    </Container>
  );
};

export default ChartComponent;
