import { sql } from "drizzle-orm";
import { connection } from "next/server";
import { db } from "@/db";

export async function GET() {
  await connection();

  let database = true;
  try {
    await db.execute(sql`select 1`);
  } catch (error) {
    console.error("Health check database query failed:", error);
    database = false;
  }

  return Response.json({ status: "ok", database });
}
