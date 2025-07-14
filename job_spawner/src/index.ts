import k8s from "@kubernetes/client-node";
import { config } from "dotenv";

config();

const GEMINI_API = process.env.GEMINI_API;
const CLOUD_NAME = process.env.CLOUD_NAME;
const CLOUDINARY_API_KEY = process.env.CLOUDINARY_API_KEY;
const CLOUDINARY_API_SECRET = process.env.CLOUDINARY_API_SECRET;
const PROJECT_ID = process.env.PROJECT_ID;

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
                  {
                    name: "CLOUDINARY_API_SECRET",
                    value: CLOUDINARY_API_SECRET,
                  },
                  { name: "PROJECT_ID", value: projectId },
                ],
              },
            ],
            restartPolicy:"Never",
          },
        },
      },
    },
  });

 
}

async function main() {
  // Check for all required environment variables
  if (!GEMINI_API) {
    console.error("GEMINI_API environment variable is not defined.");
    return;
  }
  if (!CLOUD_NAME) {
    console.error("CLOUD_NAME environment variable is not defined.");
    return;
  }
  if (!CLOUDINARY_API_KEY) {
    console.error("CLOUDINARY_API_KEY environment variable is not defined.");
    return;
  }
  if (!CLOUDINARY_API_SECRET) {
    console.error("CLOUDINARY_API_SECRET environment variable is not defined.");
    return;
  }
  if (!PROJECT_ID) {
    console.error("PROJECT_ID environment variable is not defined.");
    return;
  }

  console.log("Starting job for : ", PROJECT_ID);
  await startJob(PROJECT_ID);
}

main();
