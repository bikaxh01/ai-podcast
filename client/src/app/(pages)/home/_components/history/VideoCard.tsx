"use client";

import React from "react";
import Options from "./Options";

function VideoCard({ video }: { video: any }) {
  return (
    <div className=" px-2   w-full h-[12rem]  pb-2">
      <div className=" flex  justify-between h-full items-start">
        <div className=" w-[40%] h-full  items-start justify-between flex flex-col ">
          <div className=" flex flex-col w-full  gap-2 h-full ">
            <h1 className=" text-2xl font-semibold truncate">{video.title}</h1>
            <span
              className="text-xs text-neutral-400 line-clamp-5"
              style={{
                display: "-webkit-box",
                WebkitLineClamp: 5,
                WebkitBoxOrient: "vertical",
                overflow: "hidden",
                textOverflow: "ellipsis",
              }}
            >
              {video.description}
            </span>
          </div>
          <span className="text-xs text-neutral-400">createdAt {video.createAt}</span>
        </div>
        <div className=" w-fit flex gap-1">
          <video
            controls
            muted
            src={video.img}
            onMouseOver={(event: any) => event.target.play()}
            onMouseOut={(event: any) => event.target.pause()}
            className=" rounded-2xl"
          ></video>
          <div>
            <Options />
          </div>
        </div>
      </div>
    </div>
  );
}

export default VideoCard;
