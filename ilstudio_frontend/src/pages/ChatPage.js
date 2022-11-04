import React, { useEffect, useState } from "react";
import { ChatWindow } from "../components/ChatWindow"
import { useParams } from 'react-router';

export function ChatPage(){
    const [flagHistory, setFlagHistory] = useState(false);
    const [chatHistory, setChatHistory] = useState([])
    const { chat_title } = useParams();
    // setChatTitle(chat_title)
    async function getHistory() {
        return fetch('http://localhost:8000/chat/get_chat_history/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            "chat_title": chat_title
          })
        })
          .then(data => data.json())
       }

    const handleGetHistory = async e => {
        const history = await getHistory();
        setChatHistory(history);
      }

    if(!flagHistory){
        handleGetHistory()
        setFlagHistory(true)
    }
    return(
        <ChatWindow chatTitle={chat_title} chatHistory={chatHistory} setChatHistory={setChatHistory}/>
    )
}