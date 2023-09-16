import React, { useState } from 'react';

const TextChat = ({ sendMessage }) => {
    const [message, setMessage] = useState('');

    const handleSendMessage = () => {
        if (message.trim()) {
            sendMessage(message);
            setMessage('');
        }
    };

    return (
        <div className="p-4 flex items-center">
            <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type a message..."
                className="flex-grow p-2 border border-ececf1 rounded mr-2 bg-424553 text-ececf1"
            />
            <button 
                onClick={handleSendMessage} 
                className="px-4 py-2 bg-343541 text-ececf1 rounded hover:bg-424553 transition"
            >
                Send
            </button>
        </div>
    );
};

export default TextChat;
