import React, { useState, useRef, useEffect, useCallback } from "react";
import { MessageCard } from "./MessageCard";
import { useNavigate } from 'react-router-dom';
import ReactDOM from 'react-dom';

export function ChatWindow({chatTitle, chatHistory, setChatHistory}){
    const [inputValue, setInputValue] = useState('');
    const [flagHistory, setFlagHistory] = useState(false);
    const ws = useRef(null);
    const navigate = useNavigate();

    function scroll(){
        const section = document.querySelector( '.chat_log' ).lastChild;
        section.scrollIntoView(true);
    };
    
      
    useEffect(() => {
            ws.current = new WebSocket(
                'ws://127.0.0.1:8000'
                + '/ws/chat/'
                + chatTitle
                + '/'
                + '?token='
                + JSON.parse(sessionStorage.getItem('token'))?.token
            );
            gettingData();
        return () => ws.current.close();
    }, [ws]);

    const gettingData = useCallback(() => {
        if (!ws.current) return;

        ws.current.onmessage = e => {
            const message = JSON.parse(e.data);
            setChatHistory(prevState => [...prevState, message])
            scroll()
        };
    }, []);

    useEffect(() => {
        if(!flagHistory && chatHistory.length > 0){
            scroll()
            setFlagHistory(true)
        }
    }, [chatHistory])

    function handlerSend(text){
        ws.current.send(JSON.stringify({"message": text}));
        setInputValue('');
    }

    function handleQuit(){
        navigate('/')
    }

    return (
        <div className="chat_window">
            
            <div className="chat_inner">
                <div className="chat_header">
                    <span className="quit" onClick={handleQuit}></span>
                    <h2>{chatTitle}</h2>
                    <p>участников</p>
                </div>
                <div className="chat_log">
                    {chatHistory && chatHistory.map(mess => <MessageCard key={mess.id} text={mess.text} author={mess.author} datetime={mess.created_at}/>)}
                </div>
                <div className="input_message">
                    <input id="chat-message-input" type="text" size="100" value={inputValue} placeholder="Сообщение..."
                        onChange={event => setInputValue(event.target.value)}
                        onKeyPress={(event) => {
                            if(event.key === 'Enter'){
                                handlerSend(inputValue)
                            }
                        }}
                    ></input>
                    <div className="input_submit_container"
                        onClick={() => {
                            handlerSend(inputValue)
                        }}>
                        <div id="chat-message-submit"></div>
                    </div>
                </div>
            </div>
        </div>
        
    )
}