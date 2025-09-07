import { Outlet } from "react-router-dom";
import Navbar from "../components/navbar";
import Footer from "../components/footer";
import cog from "../assets/cog.svg";
import { useSelector } from "react-redux";

function Layout() {
  const processingStatus = useSelector(
    (state) => state.processing.processingStatus,
  );
  return (
    <div className="flex layout flex-col min-h-screen relative max-w-[100vw] overflow-x-hidden">
      <Navbar />
      <div
        className={`absolute top-[-30vh] w-[100vh] h-[100vh] right-[-20vh] z-[0.5] ${processingStatus === "generating" && "animate-slow-spin"}`}
      >
        <img src={cog} className="text-gray-500 w-full h-full" />
      </div>
      <div className="flex-1 max-w-[100vw] overflow-x-hidden p-5 md:p-10 flex flex-col justify-center items-center">
        <Outlet />
      </div>
      <Footer />
    </div>
  );
}

export default Layout;
