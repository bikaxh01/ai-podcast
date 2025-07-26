import { Button } from "@/components/ui/button";
import Image from "next/image";
import React from "react";

function HeroSection() {
  return (
    <div className=" pt-[8rem] flex flex-col   items-center   h-fit space-y-16  w-full">
      <div className="  flex flex-col w-[60%]  text-center space-y-6 ">
        <h1 className=" text-6xl font-semibold">AI-Powered Podcasts, On Demand</h1>

        <p className=" font-light text-[#86979b] ">
          EchoMind is an AI-powered podcast generator that creates audio for you to listen to while traveling, working out, or just relaxing. Turn any topic into a podcast and enjoy your personalized content on the go.
        </p>
      </div>

      <div className="  w-[80%]">
        <Image
          src={
            "/hero_image.png"
          }
          alt="Image here"
          width={500}
          height={500}
          className=" w-full rounded-2xl"
        />
        <div className=" flex items-center justify-center  mt-3">
          <Button variant={"secondary"}  className="  rounded-4xl w-[30%] font-semibold bg-[#1A1A19]">Try EchoMind</Button>
        </div>
      </div>
    </div>
  );
}

export default HeroSection;
