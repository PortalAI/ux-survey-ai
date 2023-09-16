import React from 'react';
import { Button, TextField } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

function ChatInput({ currentMessage, onChange, onSend }) {
  // Logic related only to ChatInput
  return (
    <div className="input-container">
        <TextField 
        variant="outlined"
        className="message-input"
        value={currentMessage} 
        onChange={onChange}
        onKeyUp={onSend}
        placeholder="Type a message..."
        />
        <Button color="primary" onClick={console.log(' ??? ' + currentMessage)} >
            <SendIcon />
        </Button>
    </div>

  );
}

export default ChatInput;
