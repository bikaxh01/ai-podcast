"use client";
import React from "react";
import PromptInput from "./_components/promptInput/PromptInput";
import { useUser } from "@/hook/useUser";
import History from "./_components/history/History";

function Home() {
  const [user] = useUser();

  return (
    <div className="  h-full w-full gap-7 flex-col  flex items-center justify-center">
      <PromptInput userName={user ? user.userName : ""} />
      <History />
    </div>
  );
}

export default Home;
