import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    // Unit tests live next to the code. Playwright specs in tests/e2e are
    // left out because they run with their own test runner.
    include: ["src/**/*.test.ts"],
  },
});
