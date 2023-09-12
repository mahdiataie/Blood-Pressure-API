import { FC, useState } from "react";
import styled from "styled-components";
import { UserOutlined, KeyOutlined } from "@ant-design/icons";
import { Card as antdCard, Button, Input, Typography, Form, Alert } from "antd";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const { Text } = Typography;

const Container = styled.div`
  background-color: var(--light-color);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
  gap: 1rem;
`;
const Profile = styled.div`
  border: 2px solid var(--primary-color);
  border-radius: 50%;
  height: 80px;
  width: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
`;
const Card = styled(antdCard)`
  > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    gap: 20px;
  }
  > div > span {
    width: 50vw;
  }
`;
const Actions = styled.div`
  display: flex;
  justify-content: center;
  margin: 10px 0;
  gap: 10px;
`;

const Login: FC = () => {
  const [success, setSuccess] = useState<boolean | undefined>();
  const [failed, setFailed] = useState<boolean | undefined>();
  const [isError, setError] = useState<any>();
  const [userType, setUserType] = useState<string>();
  const [userName, setUserName] = useState<string>();
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const onReset = () => {
    form.resetFields();

    setSuccess(false);
    setFailed(false);
  };

  const onFinish = async (values: any) => {
    try {
      // Send a request to your backend to retrieve the token
      const response = await axios.post("http://127.0.0.1:8000/api/token/", {
        username: values.email,
        password: values.password,
      });

      // Assuming the token is returned in the response
      const token = response.data.token;
      localStorage.setItem("token", token);
      setUserType(response.data.user_type);
      setUserName(response.data.user_name);

      // Navigate to the dashboard after getting the token
      navigate("/dashboard");
      setFailed(false);
    } catch (error: any) {
      // Handle error
      console.error("Login failed:", error.message);
      setError("Username or password is incorrect");
      setFailed(true);
    }
  };

  return (
    <Container>
      <Profile>
        <UserOutlined
          style={{ fontSize: "56px", color: `var(--primary-color)` }}
        />
      </Profile>
      <Card>
        <Form
          name="basic"
          form={form}
          onFinish={onFinish}
          autoComplete="off"
          layout="vertical"
        >
          <Form.Item
            name="email"
            label="Email"
            rules={[
              {
                type: "email",
                message: "The input is not a valid E-mail!",
              },
              { required: true },
            ]}
          >
            <Input placeholder="Enter your email" prefix={<UserOutlined />} />
          </Form.Item>
          <Form.Item
            name="password"
            label="Password"
            rules={[{ required: true }]}
          >
            <Input.Password
              placeholder="Enter your password"
              prefix={<KeyOutlined />}
            />
          </Form.Item>
          <Actions>
            <Form.Item>
              {" "}
              <Button type="default" onClick={onReset}>
                Cancel
              </Button>
            </Form.Item>

            <Form.Item>
              {" "}
              <Button type="primary" htmlType="submit">
                Login
              </Button>
            </Form.Item>
          </Actions>
        </Form>
        <div>
          <Text>Don't have an account?</Text>
          <Button type="link" onClick={() => navigate("/signup")}>
            Sign up
          </Button>
        </div>
      </Card>
      {success && (
        <Alert
          message="Login was successfull. You will now be redirected to your dashboard. "
          type="success"
          showIcon
        />
      )}
      {failed && <Alert message={isError} type="error" showIcon />}
    </Container>
  );
};

export default Login;
