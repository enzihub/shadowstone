# Web app (Next.js 14)

The `-web` part of a ShadowStone project: Next.js App Router, Clerk sign-in, Stripe
subscriptions, and Drizzle on Postgres through the Neon serverless driver.

```bash
docker compose up -d          # Postgres + a local Neon HTTP proxy (ports from .env)
npm install
npm run db:migrate            # apply src/db/migrations
npm run db:seed               # optional: two invented demo users
npm run dev
```

`.env` was written by `ss create`. Fill in the Clerk and Stripe keys, or set
`NEXT_PUBLIC_DEMO_MODE=1` to use the local stand-ins in `src/demo`.

## Stripe

```bash
npm run stripe:listen         # forward webhooks to /api/webhooks/stripe
stripe fixtures "src/app/(billing)/_utils/stripe-fixtures.json" --api-key sk_test_...
```

## Database

Change `src/db/schema.ts`, then `npm run db:generate` and `npm run db:migrate`.
