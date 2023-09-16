import React from 'react';
import Message from './Message';

const Messages = ({ messages }) => {
    return (
        <div className="p-4 overflow-y-auto h-96">
            {messages.map((message, index) => (
                <Message key={index} message={message} isUser={message.isUser} />
            ))}
        </div>
    );
};

export default Messages;
