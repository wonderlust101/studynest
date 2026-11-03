import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

// next/font downloads the font at build time and serves it from your own domain.
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

// Next.js turns this exported object into <title> and <meta> tags.
export const metadata: Metadata = {
  title: "StudyNest",
  description:
    "Write notes, ask questions about them, and review what matters.",
};

// The root layout wraps every page and must render <html> and <body>.
// `LayoutProps` is a global type that Next.js generates from your routes.
export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${geistSans.variable} h-full antialiased`}>
      <body className="flex min-h-full flex-col">{children}</body>
    </html>
  );
}
