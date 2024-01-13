/** @type {import('next').NextConfig} */

const nextConfig = {
    reactStrictMode: false,
    rewrites: () => {
      return [
        {
          source: "/api/:path*",
          destination: "http://localhost:8000/api/:path*",
        },
      ]
    },
  }

module.exports = nextConfig
