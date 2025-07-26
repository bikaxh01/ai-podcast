"use client";
import React from "react";
import Image from "next/image";

import { UserButton, useUser } from "@clerk/nextjs";
import { Button } from "@/components/ui/button";
import Link from "next/link";

function Nav({ isLanding }: { isLanding: boolean }) {
  const { isSignedIn } = useUser();

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
        <span className="  font-semibold text-2xl  ">EchoMind</span>
      </div>
      {isSignedIn ? (
        <>
          <div className=" flex space-x-4">
            {isLanding && (
              <Link
                href={"/home"}
                className=" border-primary rounded-4xl px-4 py-2 border"
              >
                Dashboard
              </Link>
            )}
            <UserButton />
          </div>
        </>
      ) : (
        <div className=" flex  space-x-4">
          <Link href={"/auth/sign-in"}>
            <Button >Sign-In</Button>
          </Link>
          <Link href={"/auth/sign-up"}>
            <Button >Sign-Up</Button>
          </Link>
        </div>
      )}
    </div>
  );
}

export default Nav;
