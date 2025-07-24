/* eslint-disable @typescript-eslint/no-unused-vars */

"use client";
import React, { useEffect, useState } from "react";
import PromptInput from "./_components/promptInput/PromptInput";

import History from "./_components/history/History";
import { getPodcasts } from "@/handler/project-apis";
import { useAuth } from "@clerk/nextjs";

function Home() {
  const [podcasts, setPodcasts] = useState([]);
  const { getToken } = useAuth();

  useEffect(() => {
    getData();
  }, []);

  const getData = async () => {
    try {
      const token = await getToken();
      const data = await getPodcasts(token!);
      setPodcasts(data.data);
    } catch (error: any) {
      setPodcasts([]);
    }
  };

  return (
    <div className="  h-full w-full gap-7 flex-col  flex items-center justify-center">
      <PromptInput refetch={getData} />
      <History podcasts={podcasts} />
    </div>
  );
}

export default Home;
