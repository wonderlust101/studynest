import { existsSync } from "node:fs";
import { defineConfig } from "drizzle-kit";

// drizzle-kit runs outside Next.js, so .env.local isn't loaded automatically.
// The file won't exist where variables are set another way, so check first.
if (existsSync(".env.local")) {
  process.loadEnvFile(".env.local");
}

// Neon's pooled URL can't hold the session state migrations rely on, so prefer
// the direct one. Local Docker only has DATABASE_URL.
const url = process.env.DATABASE_URL_UNPOOLED ?? process.env.DATABASE_URL;
if (!url) {
  throw new Error("DATABASE_URL is not set. Copy .env.example to .env.local.");
}

export default defineConfig({
  dialect: "postgresql",
  schema: "./src/db/schema/index.ts",
  // Migrations are SQL files that change the database step by step. Commit them.
  out: "./drizzle",
  // drizzle-kit connects directly using the dev-only `pg` package, not the proxy.
  dbCredentials: { url },
});
