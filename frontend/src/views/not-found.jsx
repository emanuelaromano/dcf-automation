import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div className="flex flex-1 flex-col gap-4 w-full">
      <div className="flex mt-20 flex-col text-center gap-4">
        <h1 className="page-title">Page Not Found</h1>
        <p className="page-subtitle">
          The page you are looking for does not exist.
        </p>
        <div className="flex justify-center w-full">
          <Link
            to="/"
            className="btn !border-white !border-3 !text-white link rounded-full w-full max-w-[300px]"
          >
            Go To Home
          </Link>
        </div>
      </div>
    </div>
  );
}

export default NotFound;
