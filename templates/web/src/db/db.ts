import { drizzle } from 'drizzle-orm/neon-http';
import { neonConfig } from '@neondatabase/serverless';

// Local development: point the Neon HTTP driver at the proxy from docker-compose.yml.
if (process.env.NEON_HTTP_ENDPOINT) {
  const endpoint = process.env.NEON_HTTP_ENDPOINT;
  neonConfig.fetchEndpoint = () => endpoint;
}

export const db = drizzle(process.env.DATABASE_URL!);
