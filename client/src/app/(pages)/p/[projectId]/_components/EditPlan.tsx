"use client";
import { Accordion } from "@/components/ui/accordion";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import React, { useEffect, useState } from "react";
import SceneDescriptionCard, {
  HandleSceneChangeProp,
} from "./sceneDescriptionCard";
import { Button } from "@/components/ui/button";
import { handleGenerateScenes } from "@/handler/project-apis";
import { toast } from "sonner";

interface ProjectMetaData {
  title: string;
  description: string;
}

interface SceneMetaData {
  animationTypes: string[];
  colorScheme: {
    background: string;
    highlights: string;
    text: string;
  };
  description: string;
  sceneTitle: string;
  sequence: number;
  visualElements: string[];
}

function EditPlan({ projectId }: { projectId: string }) {
  const [projectMetaData, setProjectMetaData] =
    useState<ProjectMetaData | null>(null);

  const [planData, setPlanData] = useState<SceneMetaData[] | []>([]);
  const [isLoading, setIsLoading] = useState(false);
  useEffect(() => {
    const rawData = localStorage.getItem(projectId);

    if (!rawData) {
      // navigate to home
      return;
    }
    const parsedData = JSON.parse(rawData);
    setPlanData(parsedData.scenesData);
    setProjectMetaData(parsedData.metaData);
  }, [projectId]);

  const handleSceneMetadataChange = (sceneData: HandleSceneChangeProp) => {
    const previousScene = planData.find(
      (scene) => scene.sequence == sceneData.sequence
    );

    if (!previousScene) return;

    const updatedSceneData: SceneMetaData = {
      ...previousScene,
      sceneTitle: sceneData.title,
      instruction: sceneData.description,
    };

    const finalPlanData = planData.map((scene) => {
      if (scene.sequence == sceneData.sequence) {
        return updatedSceneData;
      }
      return scene;
    });
    setPlanData(finalPlanData);
  };

  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      const reqBody = {
        id: projectId,
        title: projectMetaData?.title,
        description: projectMetaData?.description,
        plan: planData,
      };
      const res = await handleGenerateScenes(reqBody);
      toast.success(res.message);
    } catch (error: any) {
      toast.error(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className=" flex h-full  items-center justify-center ">
      <div className=" flex flex-col gap-4  h-full  w-[50%] p-2">
        <div>
          <h1 className=" text-2xl font-semibold">Edit Plan</h1>
        </div>

        <div>
          <h2>Project Metadata</h2>
          <Separator />

          <div className=" flex flex-col  gap-1 mt-1">
            <div className=" flex gap-2 flex-col">
              <label className="  text-xs">Title</label>
              <Input
                value={projectMetaData?.title}
                onChange={(e) =>
                  setProjectMetaData((p) => {
                    if (!p) return null;
                    return { ...p, title: e.target.value };
                  })
                }
              />
            </div>
            <div className=" flex flex-col gap-2">
              <label className=" text-xs">Description</label>
              <Input
                value={projectMetaData?.description}
                onChange={(e) =>
                  setProjectMetaData((p) => {
                    if (!p) return null;
                    return { ...p, description: e.target.value };
                  })
                }
              />
            </div>
          </div>
        </div>

        <div>
          <h2>Scenes Description</h2>
          <Separator />
          <Accordion type="single" collapsible>
            {planData.map((scene) => (
              <>
                <SceneDescriptionCard
                  handleSceneChange={handleSceneMetadataChange}
                  title={scene.sceneTitle}
                  description={scene.description}
                  sequence={scene.sequence}
                  key={scene.sequence}
                />
              </>
            ))}
          </Accordion>
        </div>
        <Button disabled={isLoading} onClick={handleSubmit}>
          Proceed to generate
        </Button>
      </div>
    </div>
  );
}

export default EditPlan;
