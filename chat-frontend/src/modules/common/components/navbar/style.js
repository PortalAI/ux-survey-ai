import {
  TextField as MuiTextField,
  IconButton as MuiIconButton,
  Avatar as MuiAvatar,
  Avatar as Logo,
  Badge,
  MenuItem,
  Box,
  Popover as MuiPopover,
  AppBar as MuiAppBar,
} from '@mui/material';
import styled from '@emotion/styled';
import { spacing } from '@mui/system';
/**
 * Styles for navigation bar component
 */

export const TextField = styled(MuiTextField)(spacing);
//
export const IconButton = styled(MuiIconButton)`
  svg {
    width: 22px;
    height: 22px;
  }
`;
//
export const Popover = styled(MuiPopover)`
  .MuiPaper-root {
    width: 300px;
    ${(props) => props.theme.shadows[1]};
    border: 1px solid ${(props) => props.theme.palette.divider};
  }
`;
//
export const Indicator = styled(Badge)`
  .MuiBadge-badge {
    background: ${(props) => props.theme.header.indicator.background};
    color: ${(props) => props.theme.palette.common.white};
  }
`;
//
export const Avatar = styled(MuiAvatar)`
  background: ${(props) => props.theme.palette.primary.main};
`;
//
export const MessageHeader = styled(Box)`
  text-align: center;
  border-bottom: 1px solid ${(props) => props.theme.palette.divider};
`;
//
export const NotificationHeader = styled(Box)`
  text-align: center;
  border-bottom: 1px solid ${(props) => props.theme.palette.divider};
`;
//
export const AppBar = styled(MuiAppBar)`
  background: ${(props) => props.theme.header.background};
  color: ${(props) => props.theme.header.color};
`;
//
export const LargeAvatar = styled(Logo)`
  width: 150px;
  height: 60px;
  text-align: left;
`;
//
export const SmallAvatar = styled(Logo)`
  margin-top: 15px;
  width: 100px;
  text-align: left;
`;
//
export const MenuItemDropdownItem = styled(MenuItem)`
  background: ${(props) => props.theme.header.background};
  color: ${(props) => props.theme.header.color};
`;
