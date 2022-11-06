import { BrowserRouter as Router,Routes,Route } from "react-router-dom";
import ATMCam from "./pages/atmcam";
import CCTV from "./pages/cctv";
import Login from "./pages/login";
import Anomaly from "./pages/anomaly"

const App = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Login />} />
        <Route exact path="/cctv" element={<CCTV />} />
        <Route exact path="/atmcam" element={<ATMCam />} />
      </Routes>
    </Router>
  )
}

export default App;
