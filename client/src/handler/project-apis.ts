"use server"

import axios from "axios";
import { BASE_URL } from "./user-apis";
import { cookies } from "next/headers";


export async function createPodcast(data: FormData) {
  console.log("🚀 ~ createPodcast ~ data:", data);
  try {
    const res = await axios.post(`${BASE_URL}/create-podcast`, data, {
      withCredentials: true,
    });

    return res.data;
  } catch (error: any) {
    throw new Error(error.response.data.message || "something went wrong");
  }
}

export async function getPodcasts() {
  try {
     const cookie = await cookies()
     const token = await cookie.get("__session")
     console.log("🚀 ~ getPodcasts ~ token:", token?.value)
    const res = await axios.get(`${BASE_URL}/get-podcasts`, {
      headers:{
        Authorization: `Bearer ${token?.value}`,
      }
    });
    return res.data;
  } catch (error: any) {
    throw new Error(error.response.data.message || "something went wrong");
  }
}
