"use client";
import React from "react";
import PromptInput from "./_components/promptInput/PromptInput";

import History from "./_components/history/History";

function Home() {


  return (
    <div className="  h-full w-full gap-7 flex-col  flex items-center justify-center">
      <PromptInput />
      <History />
    </div>
  );
}

export default Home;
