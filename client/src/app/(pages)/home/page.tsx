/* eslint-disable @typescript-eslint/no-unused-vars */

"use client";
import React, { useEffect, useState } from "react";
import PromptInput from "./_components/promptInput/PromptInput";

import History from "./_components/history/History";
import { getPodcasts } from "@/handler/project-apis";

function Home() {
  const [podcasts, setPodcasts] = useState([]);

  useEffect(() => {
    getData();
  }, []);

  const getData = async () => {
    try {
      const data = await getPodcasts();
      console.log("🚀 ~ getData ~ data:", data);
      setPodcasts(data.data);
    } catch (error:any) {
      setPodcasts([]);
    }
  };

  return (
    <div className="  h-full w-full gap-7 flex-col  flex items-center justify-center">
      <PromptInput refetch={getData } />
      <History podcasts={podcasts} />
    </div>
  );
}

export default Home;
