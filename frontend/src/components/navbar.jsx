import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav className="fixed top-0 right-0 w-full flex p-6 pb-0 z-10">
      <div
        className={`navbar rounded-full transition-all duration-200 ${
          scrolled ? "backdrop-blur-md bg-white/80 shadow-md" : "bg-transparent"
        }`}
      >
        <Link to="/" className="logo">
          DCF Valuation
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;
