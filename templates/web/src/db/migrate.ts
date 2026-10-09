// Applies src/db/migrations through the same Neon HTTP driver the app uses.
import { config } from 'dotenv';
config({ path: '.env' });
config({ path: '.env.local' });

async function main() {
  const { migrate } = await import('drizzle-orm/neon-http/migrator');
  const { db } = await import('./db');
  await migrate(db, { migrationsFolder: './src/db/migrations' });
  console.log('migrations applied');
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
