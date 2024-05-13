import React from 'react'
import RotateLoader from "react-spinners/RotateLoader";

function Spinner() {
  return (
    <div className="flex flex-col items-center justify-center w-full h-full">
        <RotateLoader color="#36d7b7" />
    </div>
)
}

export default Spinner