import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

// Import `env` from here instead of reading process.env directly, so a missing
// or malformed variable fails with a clear error.
export const env = createEnv({
  // Server variables are never sent to the browser. Browser-visible variables
  // would go in a `client` block and must start with NEXT_PUBLIC_.
  server: {
    DATABASE_URL: z.url(),
  },
  // Next.js inlines NEXT_PUBLIC_ variables at build time, so each one has to be
  // listed here by name. Server variables are read from process.env for us.
  experimental__runtimeEnv: {},
  // Treat `FOO=` in an env file as missing rather than as a valid empty string.
  emptyStringAsUndefined: true,
  // CI sets this for lint, typecheck and test, none of which touch the database.
  skipValidation: Boolean(process.env.SKIP_ENV_VALIDATION),
});
