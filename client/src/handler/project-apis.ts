import axios from "axios";
import { BASE_URL } from "./user-apis";

export async function createProject(prompt: string) {
  try {
    const res = await axios.post(
      `${BASE_URL}project/create-project`,
      {
        prompt,
      },
      {
        withCredentials: true,
      }
    );

    return res.data;
  } catch (error: any) {
    throw new Error(error.response.data.message || "something went wrong");
  }
}

export async function handleGenerateScenes(projectMetaData: any) {
  try {
    const res = await axios.post(
      `${BASE_URL}project/generate-scenes`,
      {
        ...projectMetaData,
      },
      {
        withCredentials: true,
      }
    );

    return res.data;
  } catch (error: any) {
    throw new Error(error.response.data.message || "something went wrong");
  }
}
