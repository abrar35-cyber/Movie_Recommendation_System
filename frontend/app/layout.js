import "./globals.css";

export const metadata = {
  title: "CineMatch | AI Movie Recommendations",
  description:
    "Discover your next favorite movie with CineMatch AI."
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}