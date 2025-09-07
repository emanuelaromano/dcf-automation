import { useSelector, useDispatch } from "react-redux";
import { setActiveTab } from "../store/slices/sidebar";

function Sidebar() {
  const activeTab = useSelector((state) => state.sidebar.activeTab);
  const dispatch = useDispatch();

  return (
    <div className="fixed top-[9rem] left-0 h-[calc(100vh-15rem)] w-1/6 border-r border-gray-200">
      <div className="flex flex-col gap-2 p-4">
        <button
          onClick={() => dispatch(setActiveTab("scheduler"))}
          className={`w-full text-left border-1 border-gray-200/40 cursor-pointer px-4 py-2 rounded-lg transition-colors ${
            activeTab === "scheduler" && "bg-gray-100/40"
          }`}
        >
          Scheduler
        </button>
        <button
          onClick={() => dispatch(setActiveTab("call-center"))}
          className={`w-full text-left border-1 border-gray-200/40 cursor-pointer px-4 py-2 rounded-lg transition-colors ${
            activeTab === "call-center" && "bg-gray-100/40"
          }`}
        >
          Call Center
        </button>
      </div>
    </div>
  );
}

export default Sidebar;
