import React from 'react'

function Layout({children}) {
  return (
    <div className='container mx-auto flex gap-10 p-10 sm:flex-row flex-col'>{children}</div>
  )
}

export default Layout