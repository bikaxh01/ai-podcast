"use client";
import React, { useState } from "react";
import Image from "next/image";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
function Nav() {
  const [isLoggedIn, setIsLoggedIn] = useState(true);
  return (
    <div className=" items-center justify-between  h-fit w-full  py-3 px-4   rounded-md flex   gap-2 ">
      <div className="   flex gap-2 items-start justify-center">
        <Image
          alt="logo"
          src={"/logo.webp"}
          className=" size-8"
          height={100}
          width={100}
        />
        <span className="  font-semibold text-2xl  ">ManiMate</span>
      </div>
      {isLoggedIn && (
        <Avatar>
          <AvatarImage src="https://github.com/shadcn.png" />
          <AvatarFallback>CN</AvatarFallback>
        </Avatar>
      )}
    </div>
  );
}

export default Nav;
