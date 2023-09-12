import { FC, useState } from "react";
import styled from "styled-components";
import { UserOutlined, KeyOutlined, HomeOutlined } from "@ant-design/icons";
import {
  Card as antdCard,
  Button,
  Input,
  Typography,
  Select,
  Form,
  Alert,
} from "antd";
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

const Card = styled(antdCard)`
  > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    gap: 20px;
  }
  > div {
    width: 60vw;
  }
`;
const Actions = styled.div`
  display: flex;
  justify-content: center;
  gap: 10px;
  margin: 10px 0;
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

const Signup: FC = () => {
  const [success, setSuccess] = useState<boolean | undefined>();
  const [failed, setFailed] = useState<boolean | undefined>();
  const [errormessage, setErrormessage] = useState("");

  const [form] = Form.useForm();
  const navigate = useNavigate();

  const onFinish = (values: any) => {
    const data = {
      email: values.email,
      password: values.password,
      uuid: values.houseId,
      user_type: values.userType,
    };

    axios
      .post("http://127.0.0.1:8000/api/register/", data)
      .then((response: any) => {
        console.log("data", data);
        setSuccess(true);
        setFailed(false);
      })
      .catch((error) => {
        setSuccess(false);
        setFailed(true);
        setErrormessage(error.request.response);
        console.log(error.request.response);
      });
  };

  const onReset = () => {
    form.resetFields();
    setSuccess(false);
    setFailed(false);
  };

  return (
    <>
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
            <Form.Item
              name="rePassword"
              label="Repeat password"
              dependencies={["password"]}
              hasFeedback
              rules={[
                { required: true },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue("password") === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(
                      new Error(
                        "The new password that you entered do not match!"
                      )
                    );
                  },
                }),
              ]}
            >
              <Input.Password
                placeholder="repeat your password"
                prefix={<KeyOutlined />}
              />
            </Form.Item>
            <Form.Item
              name="houseId"
              label="houseId"
              rules={[{ required: true }]}
            >
              <Input placeholder="HouseId" prefix={<HomeOutlined />} />
            </Form.Item>
            <Form.Item
              name="userType"
              label="User type"
              rules={[{ required: true }]}
            >
              <Select
                defaultValue="User type"
                options={[
                  { value: "patient", label: "Patient" },
                  { value: "doctor", label: "Doctor" },
                ]}
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
                  Sign Up
                </Button>
              </Form.Item>
            </Actions>
          </Form>
          <div>
            <Text>Already have an account?</Text>
            <Button type="link" onClick={() => navigate("/login")}>
              Login
            </Button>
          </div>
        </Card>
        {success && (
          <Alert
            message="Account is created successfully. "
            type="success"
            showIcon
          />
        )}
        {failed && <Alert message={errormessage} type="error" showIcon />}
      </Container>
    </>
  );
};

export default Signup;
