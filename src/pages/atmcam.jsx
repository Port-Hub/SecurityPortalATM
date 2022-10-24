import Layout from "../components/layout"
import { Link } from "react-router-dom"
const ATMCam = () => {
    return(
        <Layout>
            <div>
                <h3 className="text-2xl text-center">ATM Camera</h3>
            </div>
            <img src="http://localhost:5000/atmcam"/>
            <div className="flex flex-row text-center">
                <Link to="/" className="rounded-lg w-full py-2 px-6 bg-sky-300">Log out</Link>
            </div>
        </Layout>
    )
}

export default ATMCam