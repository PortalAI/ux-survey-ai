import React from 'react';
import { Button, TextField, Box, AppBar, Toolbar, Typography, List, ListItem, Divider } from '@mui/material';

function MessageList({ messages }) {
  return (
    <div className="message-container">
        <List>
            {messages.map((message, idx) => (
            <div key={idx}>
                <ListItem>
                {message}
                </ListItem>
                {idx !== messages.length - 1 && <Divider />}
            </div>
            ))}
        </List>
    </div>
  );
}

export default MessageList;
