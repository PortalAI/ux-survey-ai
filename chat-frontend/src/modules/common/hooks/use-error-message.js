import { useCallback, useState } from 'react';

const useAuthErrors = () => {
  const [message, setErrorMessage] = useState('');
  const generateError = useCallback((notification) => {
    switch (notification?.message) {
      case 'Token expired':
        setErrorMessage('Your link has expired. Please request new password reset link.');
        break;
      case 'Token already used':
        setErrorMessage('Your link was already used. Please request new password reset link.');
        break;
      case '"token" is not allowed to be empty':
        setErrorMessage(
          'The system does not support cross-browser password resetting. Please request for a new password reset link and reset the password in the same browser as the password reset page.'
        );
        break;
      default:
        setErrorMessage('Something went wrong');
    }
  });
  return { generateError, message };
};
export default useAuthErrors;
