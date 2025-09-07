import { useSelector } from "react-redux";

function StatusBanner() {
  const status = useSelector((state) => state.processing.bannerStatus);

  if (!status) return null;

  const getStatusConfig = () => {
    switch (status.type) {
      case "success":
        return {
          bgColor: "bg-green-50",
          borderColor: "border-green-200",
          textColor: "text-green-800",
          iconColor: "text-green-600",
          zIndex: "z-[9999]",
          message: status.message,
        };
      case "error":
        return {
          bgColor: "bg-red-50",
          borderColor: "border-red-200",
          textColor: "text-red-800",
          iconColor: "text-red-600",
          zIndex: "z-[9999]",
          message: status.message,
        };
      case "warning":
        return {
          bgColor: "bg-orange-50",
          borderColor: "border-orange-200",
          textColor: "text-orange-800",
          iconColor: "text-orange-600",
          zIndex: "z-[9999]",
          message: status.message,
        };
      default:
        return null;
    }
  };

  const config = getStatusConfig();
  if (!config) return null;

  return (
    <div
      className={`fixed top-6 right-5 z-[99999] px-6 py-4 rounded-lg border-2 ${config.bgColor} ${config.borderColor} shadow-lg backdrop-blur-sm transition-all duration-300 ease-in-out`}
    >
      <div className="flex items-center gap-3">
        {status.type === "success" && (
          <svg
            className={`w-5 h-5 ${config.iconColor}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        )}

        {status.type === "error" && (
          <svg
            className={`w-5 h-5 ${config.iconColor}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        )}

        {status.type === "warning" && (
          <svg
            className={`w-5 h-5 ${config.iconColor}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
            />
          </svg>
        )}

        <span className={`font-medium ${config.textColor}`}>
          {config.message}
        </span>
      </div>
    </div>
  );
}

export default StatusBanner;
