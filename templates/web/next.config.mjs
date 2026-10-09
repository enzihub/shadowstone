import path from 'node:path';

const demo = process.env.NEXT_PUBLIC_DEMO_MODE === '1';
const here = path.dirname(new URL(import.meta.url).pathname);

/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack(config) {
    if (demo) {
      // Demo mode: swap Clerk and Stripe for local stand-ins (src/demo). The database stays real.
      Object.assign(config.resolve.alias, {
        '@clerk/nextjs$': path.join(here, 'src/demo/clerk.tsx'),
        '@clerk/nextjs/server$': path.join(here, 'src/demo/clerk-server.ts'),
        'stripe$': path.join(here, 'src/demo/stripe.ts'),
        '@stripe/stripe-js$': path.join(here, 'src/demo/stripe-js.ts'),
      });
    }
    return config;
  },
};

export default nextConfig;
