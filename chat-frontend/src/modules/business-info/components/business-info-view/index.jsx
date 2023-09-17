/* eslint-disable react/no-array-index-key */
import { useDispatch, useSelector } from 'react-redux';
import { Loader } from 'modules/common/components';
import { selectChatState, selectLoader, selectSurveyInfo } from 'modules/business-info/selectors';
import { Avatar, Grid, IconButton, TextField, Typography } from '@mui/material';
import { SendSharp } from '@mui/icons-material';
import { useEffect, useState } from 'react';
import { blue } from '@mui/material/colors';
import { businessInfoActions } from 'modules/business-info/slice';
import { useNavigate } from 'react-router-dom';

const BusinessInfoView = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const loading = useSelector(selectLoader);
  const surveyInfo = useSelector(selectSurveyInfo);
  const chatState = useSelector(selectChatState);

  const [msg, setMsg] = useState('');
  const [businessInfo, setBusinessInfo] = useState({
    business_name: '',
    business_description: '',
    survey_name: '',
    survey_description: '',
  });
  useEffect(() => {
    if (surveyInfo && chatState.length === 8) {
      dispatch(
        businessInfoActions.setChatState({
          message: (
            <>
              <span>
                Survey link :{' '}
                <button type="button" onClick={() => navigate(surveyInfo.survey_link)}>
                  {surveyInfo.survey_link}
                </button>
              </span>{' '}
              <br />
              <span>
                {' '}
                Presentation link :{' '}
                <button type="button" onClick={() => navigate(surveyInfo.presentation_link)}>
                  {surveyInfo.presentation_link}
                </button>
              </span>
            </>
          ),
          role: 'system',
        })
      );
    }
  }, [surveyInfo]);
  useEffect(() => {
    setTimeout(() => {
      if (chatState?.length > 1 && chatState.length % 2 === 0) {
        if (chatState.length === 2) {
          setBusinessInfo({
            ...businessInfo,
            business_name: chatState[1].message,
          });
          dispatch(
            businessInfoActions.setChatState({
              message: 'Cool. Can you give me a description of your business? ',
              role: 'system',
            })
          );
        }
        if (chatState.length === 4) {
          setBusinessInfo({
            ...businessInfo,
            business_description: chatState[3].message,
          });
          dispatch(
            businessInfoActions.setChatState({
              message: 'Please provide your survey name ',
              role: 'system',
            })
          );
        }
        if (chatState.length === 6) {
          setBusinessInfo({
            ...businessInfo,
            survey_name: chatState[5].message,
          });
          dispatch(
            businessInfoActions.setChatState({
              message: 'Great! Can you give me your survey description? ',
              role: 'system',
            })
          );
        }
        if (chatState.length === 8) {
          setBusinessInfo({
            ...businessInfo,
            survey_description: chatState[7].message,
          });
        }
      }
    }, 2000);
  }, [chatState?.length]);
  //
  useEffect(() => {
    if (
      businessInfo.business_name &&
      businessInfo.business_description &&
      businessInfo.survey_name &&
      businessInfo.survey_description
    ) {
      dispatch(businessInfoActions.createSurvey(businessInfo));
    }
  }, [businessInfo]);
  // set user chat messages in chat array
  const sendChatMessageObj = async (event) => {
    event.preventDefault();
    if (msg) {
      dispatch(
        businessInfoActions.setChatState({
          message: msg,
          role: 'user',
        })
      );
      setMsg('');
    }
  };
  //
  return (
    <Loader loading={loading}>
      <Grid
        sx={{
          backgroundColor: '#f5f5f5',
          borderRadius: 5,
          boxShadow: 9,
          p: 3,
        }}
      >
        <Grid sx={{ width: '100%', height: '75vh', overflowY: 'scroll', mx: 1 }}>
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
      <form style={{ width: '100%', position: 'fixed' }}>
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
    </Loader>
  );
};
//
export default BusinessInfoView;
