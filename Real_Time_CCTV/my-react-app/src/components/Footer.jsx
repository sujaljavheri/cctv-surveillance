import React, { useContext } from 'react'
import { DataContext } from '../context/userContext'
const Footer = () => {
  const data = useContext(DataContext)
  return (
    <div>
      <h1>Footer {data}</h1>
    </div>
  )
}

export default Footer