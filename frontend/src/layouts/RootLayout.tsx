import { Outlet } from "react-router-dom";
import Navbar from "@/layouts/Navbar";
import Footer from "@/layouts/Footer";

export default function RootLayout() {
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
