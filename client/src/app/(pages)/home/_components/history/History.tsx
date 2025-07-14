"use client";
import { Separator } from "@/components/ui/separator";
import React from "react";
import VideoCard from "./VideoCard";

function History() {
  const videos = Array.from({ length: 10 }, (_, i) => ({
    img: "https://www.w3schools.com/html/mov_bbb.mp4",
    title: `Kafka for Beginner - Part ${i + 1}`,
    description:
      "Rang se rang mile Nai nai dhang khile Khushi aaj ghar mere daale hai dhera Peehu peehu papiha rate Kuhu kuhu koyal jape Aangan aagan hai pariyon ne ghera Anhat naat Bajaao sab milat Aaj mere piya ghar aavenge Rang se rang mile Nai nai dhang khile Khushi aaj ghar mere daale hai dhera Peehu peehu papiha rate Kuhu kuhu koyal jape Aangan aagan hai pariyon ne ghera Anhat naat Bajaao sab milat Aaj mere piya ghar aavenge",
    createAt: `2023-01-${(i + 1).toString().padStart(2, "0")}`,
  }));
  return (
    <div className="  w-full flex flex-col items-center justify-center">
      <div className="  flex  flex-col gap-4 w-[50%]">
        <div className=" flex flex-col gap-2 ">
          <h1 className=" text-2xl ">videos</h1>
          <Separator />
        </div>
        <div className=" flex flex-col gap-2">
          {videos.map((video) => (
            <>
              <VideoCard key={video.title} video={video} />
            </>
          ))}
        </div>
      </div>
    </div>
  );
}

export default History;
