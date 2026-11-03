import type { NextConfig } from "next";

// Importing this runs the validation, so a missing variable fails `next build`
// instead of surfacing later as a runtime error.
import "./src/lib/env";

const nextConfig: NextConfig = {
  // Data fetching runs at request time unless you opt in to caching with the
  // `use cache` directive. create-next-app enables both flags by default.
  cacheComponents: true,
  partialPrefetching: true,
  // How create-next-app wires Tailwind into Turbopack, the Next.js bundler.
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
