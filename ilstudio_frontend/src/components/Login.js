import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

async function loginUser(credentials) {
    return fetch('http://localhost:8000/chat/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json())
   }

export default function Login({ setToken, setUsername}) {
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();

    const navigate = useNavigate();
    const handleSubmit = async e => {
        e.preventDefault();
        const token = await loginUser({
          username,
          password
        });
        setToken(token);
        sessionStorage.setItem('username', username);
        navigate('')
      }
  return(
    <div className='form_container'>
      <form onSubmit={handleSubmit} className="form">
        <p>Авторизация</p>
        <label>
          <input type="text" placeholder='Логин' onChange={e => setUserName(e.target.value)} />
        </label>
        <label>
          <input type="password" placeholder='Пароль' onChange={e => setPassword(e.target.value)}/>
        </label>
        <div>
          <button type="submit">Войти</button>
        </div>
      </form>
    </div>
  )
}