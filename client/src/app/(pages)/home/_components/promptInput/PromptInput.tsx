"use client";
import { Button } from "@/components/ui/button";
import { createProject } from "@/handler/project-apis";
import { useRouter } from "next/navigation";

import React, { useEffect, useRef, useState } from "react";
import { toast } from "sonner";

function PromptInput({ userName }: { userName: string }) {
  const [isInputActive, setIsInputActive] = useState(true);
  const [disableSubmit, setSubmitDisable] = useState(false);
  const [prompt, setPrompt] = useState("");
  const router = useRouter();
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    if (!prompt) {
      setSubmitDisable(true);
    } else {
      setSubmitDisable(false);
    }
  }, [prompt]);

  const handleActivate = (isActive: boolean) => {
    setIsInputActive(isActive);
  };

  const handleSubmit = async () => {
    try {
      setSubmitDisable(true);
      const res = await createProject(prompt);
      localStorage.setItem(res.data.id, JSON.stringify(res.plan));
      router.push(`/p/${res.data.id}`);
      toast.success(res.message);
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      setSubmitDisable(false);
    }
  };
  return (
    <div className="   w-full flex flex-col  gap-4  items-center   mt-16 ">
      <div className=" text-3xl font-semibold  flex flex-col gap-2 w-[50%]">
        <h1>Hello {userName}</h1>
        <h1 className=" text-[#c2aafb]">Welcome back,</h1>
      </div>
      <div
        className={`flex flex-col  gap-2 rounded-3xl p-2 bg-[#1a1d1e] border w-[50%]  ${
          isInputActive && "border-neutral-600"
        }`}
      >
        <textarea
          ref={inputRef}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onBlur={() => handleActivate(false)}
          onClick={() => handleActivate(true)}
          className=" border-none outline-none resize-none w-full   px-2 py-4 text-white "
          placeholder="Enter you prompt here..."
        />
        <div className=" w-full  flex items-end justify-end">
          <Button
            className="  bg-[#151718] hover:bg-[#0a0b0b] rounded-full py-2 cursor-pointer w-fit"
            disabled={disableSubmit}
            onClick={handleSubmit}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="3"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="lucide lucide-move-up-icon lucide-move-up"
            >
              <path d="M8 6L12 2L16 6" />
              <path d="M12 2V22" />
            </svg>
          </Button>
        </div>
      </div>
    </div>
  );
}

export default PromptInput;
