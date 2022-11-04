import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom'
import { HomePage } from './pages/HomePage'
import { ChatPage } from './pages/ChatPage'
import  Login  from './components/Login'
import useToken from './hooks/useToken';

function App() {
  const { token, setToken } = useToken();

  if(!token) {
    return <Login setToken={setToken}/>
  }
  return (
     <Routes>
        <Route path='/' element={<HomePage/>}/>
        <Route path='/chat/:chat_title' element={<ChatPage/>}/>
      </Routes>
  );
}

export default App;
