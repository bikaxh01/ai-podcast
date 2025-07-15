import axios from "axios";
import { BASE_URL } from "./user-apis";

export async function createPodcast(data: FormData) {
  console.log("🚀 ~ createPodcast ~ data:", data);
  try {
    const res = await axios.post(
      `${BASE_URL}/create-podcast`,data,
      {
        withCredentials: true,
      }
    );

    return res.data;
  } catch (error: any) {
    throw new Error(error.response.data.message || "something went wrong");
  }
}
