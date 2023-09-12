
import { ConfigProvider } from 'antd';
import './App.css';
import AppRoutes from './pages/Routes';


function App() {

  return (

    <ConfigProvider
      theme={{
        token: {
          colorPrimary: `#69a6a0`,
        },
      }}
    >
      <AppRoutes />
    </ConfigProvider>

  );
}

export default App;
