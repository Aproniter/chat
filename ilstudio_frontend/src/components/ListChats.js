import { useNavigate } from 'react-router-dom';

export function ListChats({chats}){
    
    const navigate = useNavigate();

    function handleNavigate(path){
        
        if(path.target.outerText){
            navigate('/chat/' + path.target.outerText)
        } else {
            navigate('/chat/' + path.target.parentNode.outerText)
        }
    }
      

    return(
        <>
        {chats && chats.map(chat => 
            <span className="list_chat_item" onClick={handleNavigate}>
                <h2 className="title">
                    {chat.title}
                </h2>
                <span className="arrow"></span>
            </span>
        )}
        </>
    )
}