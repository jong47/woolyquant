// import { useState } from "react"
// import reactLogo from "./assets/react.svg"
// import viteLogo from "/vite.svg"
import "./App.css"
import Footer from "./common/Footer";
import Navigation from "./common/Navigation";

function App() {
  return (
    <>
      <div className="flex flex-col max-w-2xl">
        
        {/* Login form */}
        <div className="flex flex-row m-0">
          <Navigation />
        </div>

        {/* Landing Page */}
        <div className="">
          <h1 className="text-3xl font-bold text-center">Welcome to Wooly Quant</h1>
          <p className="text-xl text-center">The best place to find all your quantitative finance needs</p>
        </div>

        {/* Footer */}
        <div className="flex flex-row">
          <Footer />
        </div>
      </div>
    </>
  )
}

export default App;