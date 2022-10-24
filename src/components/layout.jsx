const Layout = (props) => {
    return (
        <div className="flex flex-col h-screen top-1/2 items-center justify-center">
            <form className=" bg-gradient-to-r from-cyan-400 to-cyan-600 space-y-8 rounded-2xl p-20 shadow-2xl shadow-sky-400">
                {props.children}
            </form>
        </div>
    )
}

export default Layout