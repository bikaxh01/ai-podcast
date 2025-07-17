"use client";
import { Separator } from "@/components/ui/separator";
import React, { useEffect, useState } from "react";
import PodcastCard from "./PodcastCard";
import { Podcast } from "./PodcastCard";
import { getPodcasts } from "@/handler/project-apis";

function History() {
  const [podcasts, setPodcasts] = useState([]);

  useEffect(() => {
    const getData = async () => {
      try {
        const data = await getPodcasts();
        console.log("🚀 ~ getData ~ data:", data)
        setPodcasts(data.data);
      } catch (error: any) {
        setPodcasts([]);
      }
    };
    getData();
  }, []);

  return (
    <div className="  w-full flex flex-col items-center justify-center">
      <div className="  flex  flex-col gap-4 w-[50%]">
        <div className=" flex flex-col gap-2 ">
          <h1 className=" text-2xl ">PodCast&apos;s</h1>
          <Separator />
        </div>
        <div className=" flex flex-col gap-2">
          {podcasts.map((podcast: Podcast) => (
            <>
              <PodcastCard key={podcast.id} podcast={podcast} />
            </>
          ))}
        </div>
      </div>
    </div>
  );
}

export default History;
