import { createClient } from "redis";
import k8s from "@kubernetes/client-node";
import { config } from "dotenv";

config();

const GEMINI_API = process.env.GEMINI_API as string;
const CLOUD_NAME = process.env.CLOUD_NAME as string;
const CLOUDINARY_API_KEY = process.env.CLOUDINARY_API_KEY as string;
const CLOUDINARY_API_SECRET = process.env.CLOUDINARY_API_SECRET as string;
const SERVER_URL = process.env.SERVER_URL as string;


const kc = new k8s.KubeConfig();
kc.loadFromDefault();
const k8sApi = kc.makeApiClient(k8s.BatchV1Api);

async function startJob(projectId: string) {
  const res = await k8sApi.createNamespacedJob({
    namespace: "default",
    body: {
      apiVersion: "batch/v1",
      kind: "Job",
      metadata: {
        name: `processing-job-${projectId}-k8s`.toLowerCase(),
        namespace: "default",
      },
      spec: {
        ttlSecondsAfterFinished: 120,
        template: {
          spec: {
            containers: [
              {
                name: `worker-for-${projectId}-k8s`.toLowerCase(),
                image: "bikaxh01/echomind-worker:latest",
                env: [
                  { name: "GEMINI_API", value: GEMINI_API },
                  { name: "CLOUD_NAME", value: CLOUD_NAME },
                  { name: "CLOUDINARY_API_KEY", value: CLOUDINARY_API_KEY },
                  { name: "SERVER_URL", value: SERVER_URL },
                  {
                    name: "CLOUDINARY_API_SECRET",
                    value: CLOUDINARY_API_SECRET,
                  },
                  { name: "PROJECT_ID", value: projectId },
                ],
              },
            ],
            restartPolicy: "Never",
          },
        },
        backoffLimit:2
      },
      
    },
  });
}

async function main() {
  const redisClient = await createClient({
    url: process.env.REDIS_URL,
  }).connect();
  try {
    while (true) {
      const data = await redisClient.brPop("podcast", 0);
      if (!data?.element) return;
      console.log("Starting job for : ", data.element);
      await startJob(data.element);
    }
  } catch (error) {
    console.log("🚀 ~ main ~ error:", error);
  }
}

main();
