import { format } from "date-fns";

export function MessageCard({text, author, datetime}){
    let className = ["message_card"]
    let messageAuthor = author
    if(author === sessionStorage.getItem('username')){
        className = className.concat(["message_current_user"])
        messageAuthor = ''
    }
    let messageDate = new Date(datetime);
    let dateLocal = new Date(messageDate.getTime() - messageDate.getTimezoneOffset()*60*1000);
    return(
        <div className={className.join(' ')}>
            <div className="message_card_inner">
                {messageAuthor && <p className="message_author">{messageAuthor}</p>}
                <p className="message_text">{text}</p>
                <p className="message_time">{format(dateLocal, "H:mm")}</p>
            </div>
        </div>
    )
}