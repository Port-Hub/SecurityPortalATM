const Layout = (props) => {
    return (
        <div className=" font-mono flex flex-col h-screen top-1/2 items-center justify-center bg-[#FDEEDC]">
            <div className=" truncate">
            <h1 className="mb-5 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl">Bank of Baroda Security System</h1>
            </div>
            <form className=" bg-[#F1A661] space-y-8 rounded-2xl p-20 shadow-2xl shadow-neutral">
                {props.children}
            </form>
        </div>
    )
}

export default Layout