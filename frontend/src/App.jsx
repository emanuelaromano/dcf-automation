import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./layout/layout";
import NotFound from "./views/not-found";
import DCFValuation from "./views/dcf-valuation";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="" element={<DCFValuation />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
