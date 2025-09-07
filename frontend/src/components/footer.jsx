function Footer() {
  return (
    <footer className="footer sm:footer-horizontal footer-start text-[var(--text-white)] p-4">
      <aside>
        <p className="text-sm pl-[2rem]">
          Copyright © {new Date().getFullYear()} - All right reserved by Calexo
        </p>
      </aside>
    </footer>
  );
}

export default Footer;
