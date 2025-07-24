import axios from "axios";

export const BASE_URL = process.env.NEXT_PUBLIC_SERVER_BASE_URL;

export async function createPodcast(data: FormData, token: string) {
  console.log("🚀 ~ createPodcast ~ data:", data);
  try {
    const res = await axios.post(`${BASE_URL}/create-podcast`, data, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    return res.data;
  } catch (error: any) {
    throw new Error(error.response.data.message || "something went wrong");
  }
}

export async function getPodcasts(token: string) {
  try {
    const res = await axios.get(`${BASE_URL}/get-podcasts`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return res.data;
  } catch (error: any) {
    throw new Error(error.response.data.message || "something went wrong");
  }
}
