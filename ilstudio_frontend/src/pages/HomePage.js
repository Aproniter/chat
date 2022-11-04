import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import { ListChats } from '../components/ListChats'

export function HomePage(){
    const [inputValue, setInputValue] = useState('');
    const [listChats, setListChats] = useState([]);
    const [flagChat, setFlagChat] = useState(false);

    const navigate = useNavigate();

    function handleNavigate(){
        navigate('/chat/' + inputValue)
    }

    async function getChats() {
        return fetch('http://localhost:8000/chat/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
            })
          .then(data => data.json())
       }
    const handleGetChats = async e => {
        const chats = await getChats();
        setListChats(chats);
      }

    if(!flagChat){
        handleGetChats();
        setFlagChat(true);
    }

    function handleQuit(){
        sessionStorage.removeItem('username');
        sessionStorage.removeItem('token');
        window.location.reload();
    }

    return(
        <div className='form_container'>
            <span className="quit" onClick={handleQuit}></span>
            <form className="form" onSubmit={handleNavigate}>
                <p>Выберите / создайте чат</p>
                <ListChats chats={listChats}/>
                <div className="form_chat_container">
                    <label>
                        <input type="text" placeholder='Введите название чата'
                            value={inputValue}
                            onChange={event => setInputValue(event.target.value)}
                            onKeyPress={(event) => {
                                if(event.key === 'Enter'){
                                    handleNavigate();
                            }}}
                        />
                    </label>
                    <div>
                        <button type="submit">Создать</button>
                    </div>
                </div>
            </form>
        </div>
    )
}