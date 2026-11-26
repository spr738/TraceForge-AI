import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TraceForge AI | Observability",
  description: "Application monitoring and incident intelligence dashboard"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
