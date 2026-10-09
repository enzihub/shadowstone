// Demo rows with invented people. Run: npm run db:seed
import { config } from 'dotenv';
config({ path: '.env' });
config({ path: '.env.local' });

async function main() {
  const { db } = await import('./db');
  const { users, userPrefs } = await import('./schema');
  const people = [
    { clerkId: 'user_demo_ada', fullName: 'Ada Park', email: 'ada@example.com' },
    { clerkId: 'user_demo_leo', fullName: 'Leo Marsh', email: 'leo@example.com' },
  ];
  for (const p of people) {
    const [u] = await db.insert(users).values(p).onConflictDoNothing().returning();
    if (u) await db.insert(userPrefs).values({ userId: u.id, email: u.email, timezone: 'UTC' }).onConflictDoNothing();
  }
  console.log(`seeded ${people.length} demo users`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
