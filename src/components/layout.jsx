import Bob from "../assets/Bobpng.png";
const Layout = (props) => {
  return (
    <div className="flex flex-col h-screen items-center bg-[#FDEEDC]">
      <div className="flex flex-row ">
        <div className="flex-row m-0 ">
          <img className=" mb-16 mt-10 align-center" src={Bob} alt="bob" />
        </div>
        {/* <div className="flex-row truncate mt-10">
          <h1 className="mb-16 mt-5 text-4xl tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl">
            Bank of Baroda Security Portal
          </h1>
        </div> */}
      </div>

      <form className=" bg-[#ff5b35] space-y-8 rounded-2xl p-20 drop-shadow-xl    ">
        {props.children}
      </form>
    </div>
  );
};

export default Layout;
