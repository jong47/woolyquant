import { CiUser } from "react-icons/ci";
// import { IoSettingsOutline } from "react-icons/io5";

function Navigation() {
  return (
    <>
      <div className="flex flex-row text-center m-0 md:space-x-6">
        <div className="flex float-left">
          <a href="/">Wooly Quant</a>
        </div>
        <div id="dropdown-trading" className="">
          <a href="/trading/bot">Trading Bot</a>
        </div>
        <a href="/dashboard">Dashboard</a>
        <a href="/marketplace">Marketplace</a>
        <a href="/about">What We're About</a>
        {/* <a href="/settings"><IoSettingsOutline /></a> */}
        <a id='active' href="/profile"><CiUser /></a>
      </div>
    </>
  );
}

export default Navigation;