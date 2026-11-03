import { neon, neonConfig } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-http";
import { env } from "@/lib/env";

// Locally, send queries to the proxy from docker-compose.yml. Any other host,
// such as Neon in production, keeps the driver's default endpoint.
const LOCAL_DB_HOST = "db.localtest.me";
if (new URL(env.DATABASE_URL).hostname === LOCAL_DB_HOST) {
  neonConfig.fetchEndpoint = `http://${LOCAL_DB_HOST}:4444/sql`;
}

// Each query is a separate HTTP request, so there is no connection pool to
// manage, which suits serverless. Interactive transactions need the driver's
// WebSocket mode instead.
const client = neon(env.DATABASE_URL);

// Drizzle is the ORM. Unlike Mongoose, it writes SQL for you rather than
// hiding it, and you'll pass your tables in here once they exist.
export const db = drizzle({ client });
