/* eslint-disable react/no-array-index-key */
import { useDispatch, useSelector } from 'react-redux';
import { InvalidSlug, Loader } from 'modules/common/components';
import { Avatar, Grid, IconButton, Paper, TextField, Typography } from '@mui/material';
import { SendSharp } from '@mui/icons-material';
import { useEffect, useState } from 'react';
import { blue } from '@mui/material/colors';
import { useParams } from 'react-router-dom';
import { chatActions } from 'modules/chat/slice';
import useWebSocket from 'react-use-websocket';
import { ENVIRONMENT } from 'config';
import { selectIsInvalidSurveyId, selectLoader } from 'modules/chat/selectors';

const ChatView = () => {
  const dispatch = useDispatch();
  const { surveyId } = useParams();
  //
  const loading = useSelector(selectLoader);
  const IsInvalidSurveyId = useSelector(selectIsInvalidSurveyId);
  //
  const [msg, setMsg] = useState('');
  const [chatState, setChatState] = useState([]);
  //
  const socketUrl = `${ENVIRONMENT.WEB_SOCKET_URL}/${surveyId}`;
  //
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl, {
    onOpen: () => console.log('opened'),
    // Will attempt to reconnect on all close events, such as server shutting down
    shouldReconnect: () => true,
  });
  //
  useEffect(() => {
    dispatch(chatActions.validateSurveyLinkId({ surveyId }));
  }, [surveyId]);
  //
  useEffect(() => {
    if (lastMessage) {
      setChatState([
        ...chatState,
        {
          message: lastMessage.data.replace('bot responded:', '').trim(),
          role: 'auto',
        },
      ]);
    }
  }, [lastMessage]);
  // set user chat messages in chat array
  const sendChatMessageObj = async (event) => {
    event.preventDefault();
    if (readyState === 1 && msg) {
      sendMessage(msg);
      setChatState([
        ...chatState,
        {
          message: msg,
          role: 'user',
        },
      ]);
      setMsg('');
    }
  };
  //
  return (
    <Loader loading={loading}>
      {IsInvalidSurveyId ? (
        <InvalidSlug
          message="Invalid survey ID received."
          description="We apologize for the inconvenience, but it seems that the survey ID you provided is 
          not recognized by our system. To successfully access or participate in the survey, please make sure to use a valid and correctly formatted survey ID."
        />
      ) : (
        <>
          <Grid sx={{ backgroundColor: 'darkblue', borderRadius: 5, py: 3, mb: 1 }}>
            <Paper sx={{ backgroundColor: 'darkblue', ml: 4, alignItems: 'center' }}>
              <Typography color="white" variant="h6">
                Chat survey ID: {surveyId}
              </Typography>
            </Paper>
          </Grid>
          <Grid
            sx={{
              backgroundColor: '#f5f5f5',
              borderRadius: 5,
              boxShadow: 9,
              p: 3,
            }}
          >
            <Grid sx={{ width: '100%', height: '70vh', overflowY: 'scroll', mx: 1 }}>
              {chatState?.map((item, index) => (
                <Grid
                  key={index}
                  container
                  flexDirection="row"
                  item
                  xs={8}
                  width="fit-content"
                  style={{
                    padding: 5,
                    borderRadius: 10,
                    marginTop: 5,
                    backgroundColor: item.role === 'system' ? '#2e384a' : '#e0e0e0',
                    marginLeft: item.role === 'user' ? 'auto' : 0,
                    marginRight: item.role === 'system' ? 'auto' : 0,
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}
                >
                  <Avatar sx={{ bgcolor: blue[500] }} variant="circular">
                    {item.role === 'user' ? 'U' : 'B'}
                  </Avatar>
                  <Typography
                    fontSize={16}
                    sx={{ color: item.role === 'system' ? 'white' : 'black', mx: 3 }}
                  >
                    {item.message}
                  </Typography>
                </Grid>
              ))}
            </Grid>
          </Grid>
          <form style={{ width: '100%', paddingBottom: '100px' }}>
            <Grid container flexDirection="row" sx={{ mt: 4 }}>
              <Grid item xs={11}>
                <TextField
                  fullWidth
                  type="text"
                  placeholder="Type a message.."
                  InputProps={{ sx: { borderRadius: 5, backgroundColor: '#e0e0e0', fontSize: 16 } }}
                  value={msg}
                  onChange={(e) => setMsg(e.target.value)}
                />
              </Grid>
              <Grid container item xs={1} justifyContent="left">
                <IconButton type="submit" onClick={sendChatMessageObj} disabled={msg === ''}>
                  <SendSharp fontSize="large" />
                </IconButton>
              </Grid>
            </Grid>
          </form>
        </>
      )}
    </Loader>
  );
};
//
export default ChatView;
