import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'www.w3schools.com',
      },
      {
        protocol: 'https',
        hostname: 'www.manuscdn.com',
      },
      {
        protocol: 'https',
        hostname: 'files.manuscdn.com',
      },
    ],
  },
};

export default nextConfig;
