const Layout = (props) => {
    return (
        <div className="flex flex-col h-screen top-1/2 items-center justify-center">
            <form className=" bg-gradient-to-r from-sky-900 to-sky-900 space-y-8 rounded-2xl p-20 shadow-2xl shadow-sky-400">
                {props.children}
            </form>
        </div>
    )
}

export default Layout