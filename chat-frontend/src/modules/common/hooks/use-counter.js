/* eslint-disable consistent-return */
import ROUTES from 'modules/common/constants/route';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const useCounter = () => {
  const navigate = useNavigate();
  const [timeLeft, setTimeLeft] = useState(null);
  useEffect(() => {
    if (timeLeft === 0) {
      setTimeLeft(null);
      navigate(ROUTES.LOGIN);
    }

    /* Exit early when we reach 0 */
    if (!timeLeft) return;

    /* Save intervalId to clear the interval when the
        component re-renders */
    const intervalId = setInterval(() => {
      setTimeLeft(timeLeft - 1);
    }, 1000);

    /* Clear interval on re-render to avoid memory leaks */
    return () => clearInterval(intervalId);
    /* Add timeLeft as a dependency to re-rerun the effect
        when we update it */
  }, [timeLeft, navigate]);
  return { timeLeft, setTimeLeft };
};
export default useCounter;
