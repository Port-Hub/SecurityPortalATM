import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faPeopleGroup, faKey, faCamera } from "@fortawesome/free-solid-svg-icons"
import { Link } from "react-router-dom"
import Layout from "../components/layout"
import { useRef, useState } from "react"

const Login = () => {

    const mList = [
        {
            "name": "Camera 1",
            "link": "atmcam"
        },
        {
            "name": "Camera 2",
            "link": "cctv"
        }
    ]

    const [mode, setMode] = useState({"name":"ATM Camera", "link":"atmcam"});

    const mRef = useRef(mode);  

    const mChange = () => {
        if(mRef.current.value == mList[0].name)
        {
            setMode(mList[0])
        }
        else
        {
            setMode(mList[1])
        }
        console.log(mRef.current.value)
    }

    return(
        <Layout>
            <div>
                <h3 className="text-3xl text-center text-[#FDEEDC]">Security Login</h3>
            </div>
            <div className="flex flex-row items-center gap-x-2">
                <FontAwesomeIcon icon={faPeopleGroup} />
                <input className=" placeholder:text-[#FFD8A9] bg-transparent border-2 p-2 rounded-xl" type="name" placeholder="Username"></input>
            </div>
            <div className="flex flex-row gap-x-2 items-center">
                <FontAwesomeIcon icon={faKey} />
                <input className=" placeholder:text-[#FFD8A9] bg-transparent border-2 p-2 rounded-xl" type="password" placeholder="Password"></input>
            </div>
            <div className="flex flex-row gap-x-2 items-center">
                <FontAwesomeIcon icon={faCamera} />
                <select ref={mRef} onChange={mChange}  className=" placeholder:text-[#FFD8A9] bg-transparent w-full border-2 p-2 rounded-xl" type="radio">
                    <option>{mList[0].name}</option>
                    <option>{mList[1].name}</option>
                </select>
            </div>
            <div className="flex flex-row text-center">
                <Link to={mode.link} className="rounded-lg w-full py-2 px-6 bg-[#050505]">Login</Link>
            </div>
        </Layout>
    )
}

export default Login