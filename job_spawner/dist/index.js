"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const redis_1 = require("redis");
const client_node_1 = __importDefault(require("@kubernetes/client-node"));
const dotenv_1 = require("dotenv");
(0, dotenv_1.config)();
const GEMINI_API = process.env.GEMINI_API;
const CLOUD_NAME = process.env.CLOUD_NAME;
const CLOUDINARY_API_KEY = process.env.CLOUDINARY_API_KEY;
const CLOUDINARY_API_SECRET = process.env.CLOUDINARY_API_SECRET;
const SERVER_URL = process.env.SERVER_URL;
const kc = new client_node_1.default.KubeConfig();
kc.loadFromDefault();
const k8sApi = kc.makeApiClient(client_node_1.default.BatchV1Api);
function startJob(projectId) {
    return __awaiter(this, void 0, void 0, function* () {
        const res = yield k8sApi.createNamespacedJob({
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
                    backoffLimit: 2
                },
            },
        });
    });
}
function getRedisClient() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const client = yield (0, redis_1.createClient)({
                url: process.env.REDIS_URL,
            }).connect();
            console.log("🟢  connected to redis");
            return client;
        }
        catch (error) {
            console.log("🔴🔴 Unable to connect to redis");
            throw new Error("🔴🔴 Unable to connect to redis");
        }
    });
}
function main() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const redisClient = yield getRedisClient();
            while (true) {
                const data = yield redisClient.brPop("podcast", 0);
                if (!(data === null || data === void 0 ? void 0 : data.element))
                    return;
                console.log("Starting job for : ", data.element);
                yield startJob(data.element);
            }
        }
        catch (error) {
            console.log("🚀 ~ main ~ error:", error);
        }
    });
}
main();
