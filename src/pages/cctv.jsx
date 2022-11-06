import Layout from "../components/layout"
import { Link } from "react-router-dom"
import Anomaly from "./anomaly"

const CCTV = () => {
    return(
        <div className="bg-[#FDEEDC]">
            <div className="flex flex-row text-center">
                <Anomaly/>
            </div>
        </div>
    )
}

export default CCTV