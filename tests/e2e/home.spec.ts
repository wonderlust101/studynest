import { expect, test } from "@playwright/test";

test("landing page shows the StudyNest heading", async ({ page }) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { level: 1, name: "StudyNest" }),
  ).toBeVisible();
});
