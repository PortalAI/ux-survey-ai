import React, { useState } from 'react';
import TextChat from '../components/Input/TextChat';
import Messages from '../components/Messages/Messages';

const Chat = () => {
    const [messages, setMessages] = useState([]);

    const handleSendMessage = (messageContent) => {
        const newMessage = {
            content: messageContent,
            isUser: true,
        };
        setMessages(prevMessages => [...prevMessages, newMessage]);
        // Here, you can also send the message to the backend or AI and get a response.
        // for now, we'll just send a dummy response
        setTimeout(() => {
            const response = {
                content: 'This is a dummy response.',
                isUser: false,
            };
            setMessages(prevMessages => [...prevMessages, response]);
        }
        , 1000);
    };

    return (
        <div>
            <Messages messages={messages} />
            <TextChat sendMessage={handleSendMessage} className="bottom-0"/>
        </div>
    );
};

export default Chat;
