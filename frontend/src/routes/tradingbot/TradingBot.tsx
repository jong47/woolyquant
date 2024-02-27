import { FaRobot } from "react-icons/fa6";
import { CiImport } from "react-icons/ci";
import Navigation from "../../common/Navigation";
import { useQuery } from "@tanstack/react-query";

function CreateBot() {
  const query = useQuery({ 
    queryKey: ['testCall'],
    queryFn: async () => {
      fetch('http://localhost:8080/v1/healthz').then((res) => {
          let result = res.json()
          console.log(result);
          return result;
        }
      )},
  });

  return (
    <>
      {console.log(query.data)}
    </>
  )
}

function TradingBot() {


  return (
    <>
      <div className="flex flex-col space-y-10">
        <Navigation />
        <div className="flex flex-col space-y-4">
          <div className="flex flex-row items-center space-x-2">
            <FaRobot className="" />
            <button className="text-xs" onClick={() => console.log("Creating Bot!")}>Create Bot</button>
            <CreateBot />
          </div>
          <div className="flex flex-row items-center space-x-2">
            <CiImport className="" />
            <button className="text-xs" onClick={() => console.log("Importing Bot!")}>Import Bot</button>
          </div>
        </div>
      </div>
    </>
  );
}

export default TradingBot;