import React from 'react';

const Message = ({ message, isUser }) => {
    return (
        <div 
            className={`p-4 my-2 w-auto max-w-md ${isUser ? 'bg-343541 text-right ml-auto' : 'bg-424553 text-left mr-auto'} text-ececf1`}
        >
            {message.content}
        </div>
    );
};

export default Message;
