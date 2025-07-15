"use client";
import { Button } from "@/components/ui/button";
import { createPodcast } from "@/handler/project-apis";

import { useUser } from "@clerk/nextjs";
import { ChevronRight, Plus } from "lucide-react";

import { useRouter } from "next/navigation";

import React, { useEffect, useRef, useState } from "react";

import { toast } from "sonner";

function PromptInput() {
  const [isInputActive, setIsInputActive] = useState(true);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [disableSubmit, setSubmitDisable] = useState(false);
  const { user } = useUser();
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

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    try {
      e.preventDefault();
      setSubmitDisable(true);

      const newForm = new FormData();
      newForm.append("prompt", prompt);
      if (selectedFile) newForm.append("file", selectedFile);

      // send file to backend
      const res = await createPodcast(newForm);
      console.log(res);

      // toast.success(res.message);
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      setSubmitDisable(false);
    }
  };
  return (
    <div className="   w-full flex flex-col  gap-4  items-center   mt-16 ">
      <div className=" text-3xl font-semibold  flex flex-col gap-2 w-[50%]">
        <h1>
          Hello &nbsp;
          {user && user.firstName}
        </h1>
        <h1 className=" text-[#c2aafb]">Welcome back,</h1>
      </div>
      <form
        onSubmit={handleSubmit}
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
        <div className="  w-full justify-between  flex ">
          {selectedFile ? (
            <div className="max-w-28  pl-2 rounded-2xl text-xs flex items-center text-neutral-300  justify-center  border">
              {selectedFile.name ? (
                <span className=" truncate">
                  {selectedFile.name.toLowerCase()}
                </span>
              ) : (
                ""
              )}
            </div>
          ) : (
            <div>
              <label
                htmlFor="file-upload"
                className="inline-block w-full h-full pl-3   bg-[#1a1d1e] cursor-pointer "
              >
                <Plus />
              </label>
              <input
                id="file-upload"
                type="file"
                accept="application/pdf"
                className="hidden"
                onChange={(e) =>
                  setSelectedFile(e.target.files ? e.target.files[0] : null)
                }
              />
            </div>
          )}

          <Button
            className="   rounded-full py-2 cursor-pointer w-fit"
            type="submit"
            disabled={disableSubmit}
          >
            Generate
            <ChevronRight />
          </Button>
        </div>
      </form>
    </div>
  );
}

export default PromptInput;
