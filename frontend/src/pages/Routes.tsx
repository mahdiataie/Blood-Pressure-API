import { FC } from "react";
import Dashboard from "./Dashboard";
import Login from "./Login";
import { Navigate, Route, Routes } from "react-router-dom";
import Signup from "./Signup";

const AppRoutes: FC = () => {
  return (
    <Routes>
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/" element={<Navigate to="/signup" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="*" element={<Navigate to="/signup" />} />
    </Routes>
  );
};

export default AppRoutes;
