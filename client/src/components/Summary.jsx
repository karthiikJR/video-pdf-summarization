import React from 'react'

function Summary() {
  return (
    <>
       <h1 className="mb-4 text-3xl font-extrabold text-gray-900 dark:text-white md:text-5xl lg:text-6xl"><span className="text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400">Summary</span></h1>
        <p id='summary' className="mb-3 text-gray-300 ">Your generated summary will be shown here. It can be either a YouTube video or a PDF</p>        
    </>
  )
}

export default Summary