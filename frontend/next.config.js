/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8003',
    NEXT_PUBLIC_APP_NAME: 'Dashboard Educativo',
    NEXT_PUBLIC_APP_VERSION: '1.0.0'
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8003'}/api/:path*`
      }
    ]
  }
}

module.exports = nextConfig