import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

const createSurveySession = async (survey_id) => {
  try {
    const response = await axios.post(`${BASE_URL}/create_survey_session/${survey_id}`);
    return response.data;
  } catch (error) {
    console.error("Error creating survey session:", error);
    throw error;
  }
};

export default {
  createSurveySession
};
