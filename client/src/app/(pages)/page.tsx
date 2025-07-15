"use client";
import { Button } from "@/components/ui/button";
import { BASE_URL } from "@/handler/user-apis";
import axios from "axios";

import { useEffect } from "react";

export default function Home() {
  useEffect(() => {
    const test = async () => {
      const res = await axios.post(
        `${BASE_URL}/create-podcast`,
        {
          prompt: "e",
        },
        { withCredentials: true }
      );
      console.log("🚀 ~ test ~ res:", res);
    };
    test();
  }, []);
  return (
    <>
      <Button>ManiMate</Button>
    </>
  );
}
