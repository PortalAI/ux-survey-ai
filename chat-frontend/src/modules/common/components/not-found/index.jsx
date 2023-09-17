import { Typography } from '@mui/material';
import styled from '@emotion/styled';

const Wrapper = styled.div`
  padding: ${(props) => props.theme.spacing(6)};
  text-align: center;
  background: transparent;

  ${(props) => props.theme.breakpoints.up('md')} {
    padding: ${(props) => props.theme.spacing(10)};
  }
`;
/**
 * Invalid survey error component
 * @param {*} props
 * @returns
 */
const InvalidSlug = (props) => {
  const { message, description } = props;
  //
  return (
    <Wrapper>
      <Typography component="h2" variant="h5" align="center" gutterBottom>
        {message}
      </Typography>
      <Typography component="h2" variant="body1" align="center" gutterBottom>
        {description}
      </Typography>
    </Wrapper>
  );
};
//
export default InvalidSlug;
