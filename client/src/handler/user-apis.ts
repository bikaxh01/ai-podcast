import axios from "axios";

export const BASE_URL = process.env.NEXT_PUBLIC_SERVER_BASE_URL;

export async function validateUserEmail(email: string) {
  try {
    const res = await axios.get(`${BASE_URL}user/validate-email/${email}`);

    return { success: true, message: res.data.message };
  } catch (error: any) {
    return {
      success: false,
      message: error.response.data.message || "something went wrong",
    };
  }
}

export async function registerUser(
  email: string,
  userName: string,
  password: string
) {
  try {
    const res = await axios.post(`${BASE_URL}user/sign-up`, {
      email,
      userName,
      password,
    });
    return res.data;
  } catch (error: any) {
    throw new Error(error.response.data.message || "something went wrong");
  }
}

export async function handleSignIn(email: string, password: string) {
  try {
    const res = await axios.post(
      `${BASE_URL}user/sign-in`,
      {
        email,
        password,
      },
      { withCredentials: true }
    );

    return res.data;
  } catch (error: any) {
    throw new Error(error.response.data.message || "something went wrong");
  }
}
