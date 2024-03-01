import { useEffect } from "react";

function Vision(){  
  useEffect(() => {
    const webgazer = window.webgazer
    webgazer.setGazeListener((data,clock)=>{
      console.log(data,clock)
    }).saveDataAcrossSessions(false).begin()
  },[])
  return(
    <div className="App">
      Hello World
    </div>
  )
}

export default Vision