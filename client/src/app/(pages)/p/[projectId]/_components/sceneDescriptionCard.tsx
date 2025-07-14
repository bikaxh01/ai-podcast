"use client";
import React from "react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export interface HandleSceneChangeProp {
  title: string;
  description: string;
  sequence: number;
}

function SceneDescriptionCard({
  title,
  description,
  sequence,
  handleSceneChange,
}: {
  title: string;
  description: string;
  sequence: number;
  handleSceneChange: (data: HandleSceneChangeProp) => void;
}) {
  return (
    <div>
      <Accordion type="single" collapsible>
        <AccordionItem value={sequence.toString()}>
          <AccordionTrigger>
            <div className=" flex  w-full justify-between">
              <h2>{title}</h2>
              <span className="  text-xs text-neutral-500">
                scene {sequence}
              </span>
            </div>
          </AccordionTrigger>
          <AccordionContent className=" flex flex-col gap-2 ">
            <div className=" flex flex-col gap-1">
              <Label>Title</Label>
              <Input
                value={title}
                onChange={(e) =>
                  handleSceneChange({
                    title: e.target.value,
                    description: description,
                    sequence,
                  })
                }
                className="!text-xs"
              />
            </div>
            <div className=" flex-col flex gap-1">
              <Label>Description</Label>
              <Input
                value={description}
                className=" !text-xs"
                onChange={(e) =>
                  handleSceneChange({
                    title: title,
                    description: e.target.value,
                    sequence,
                  })
                }
              />
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  );
}

export default SceneDescriptionCard;
