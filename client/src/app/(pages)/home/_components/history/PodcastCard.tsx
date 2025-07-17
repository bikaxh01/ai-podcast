"use client";

import React from "react";

import { Skeleton } from "@/components/ui/skeleton";
import { formatDistanceToNowCustom } from "@/lib/utils";
import {
  Dialog,
  DialogContent,
  DialogTrigger,
} from "@/components/ui/dialog";
import AudioPlayer from "@/components/ui/audio-player";
export interface Podcast {
  id: string;
  title?: string;
  description?: string;
  status: "COMPLETED" | "PROCESSING" | "PENDING";
  audio_url?: string;
  file_url?: string;
  prompt?: string;
  user_id: string;
  created_at: string;
}

function PodcastCard({ podcast }: { podcast: Podcast }) {
  return (
    <>
      {podcast.status == "PROCESSING" || podcast.status == "PENDING" ? (
        <div>
          <div className="     w-full h-[6rem] rounded-2xl  ">
            <Skeleton className=" w-full h-full" />
          </div>
        </div>
      ) : podcast.status == "COMPLETED" ? (
        <Dialog>
          <DialogTrigger className="   w-full h-[6rem] transition delay-100   hover:border-neutral-500 border p-2 rounded-2xl">
            <div>
              <h1 className=" font-semibold">{podcast.title}</h1>

              <p className=" line-clamp-2  text-xs text-neutral-400  ">
                {podcast.description}
              </p>
              <p className=" text-[10px]  mt-2 text-neutral-500 ">
                CreatedAt:&nbsp;{formatDistanceToNowCustom(podcast.created_at)}
              </p>
            </div>
          </DialogTrigger>
          <DialogContent>
            <AudioPlayer
              src={podcast.audio_url || ""}
              cover="https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=2970&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              title={podcast.title}
            />
          </DialogContent>
        </Dialog>
      ) : null}
    </>
  );
}

export default PodcastCard;
