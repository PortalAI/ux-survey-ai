import React, { useEffect, useState, useContext } from "react";
import { useParams } from 'react-router-dom';
import { AppBar, Toolbar, Typography, ListItem, Divider } from '@mui/material';
import ChatInput from './ChatInput';
import MessageList from './MessageList';
import './ChatUI.css';
import api from '../../services/api';
import useWebSocket from '../../services/websocket';
import MyContext from '../../state/context';

function ChatUI() {
    const [messages, sendMessage] = useWebSocket('ws://127.0.0.1:8000/chat');
    const [currentMessage, setCurrentMessage] = useState('');
    const { survey_id } = useParams();
    const [globalState, setGlobalState] = useContext(MyContext);

    useEffect(() => {
      // create record
      const createSurveyRecord = async () => {
        try {
          const data = await api.createSurveySession(survey_id);
          console.log(data);
        } catch (error) {
          console.error("Error in component:", error);
        }
      };
      // get survey_id and store it global
      setGlobalState(prevState => ({
        ...prevState,
        survey_id
      }));
      createSurveyRecord();

    }, [survey_id, setGlobalState]);
  
    const clickSendMessage = (currentMessage) => {
      sendMessage(currentMessage);
      setCurrentMessage('');
    }

    return (
      <div className="app-container">
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6">
              Chat Survey ID: {survey_id}
            </Typography>
          </Toolbar>
        </AppBar>
  
        <MessageList messages={messages} />
        <ChatInput 
          currentMessage={currentMessage}
          onChange={e => setCurrentMessage(e.target.value)} 
          onSend={e => e.key === 'Enter' && clickSendMessage(currentMessage)}
        />
      </div>
    );
  }
  

export default ChatUI;
