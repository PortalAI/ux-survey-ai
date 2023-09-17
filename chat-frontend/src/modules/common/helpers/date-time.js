/**
 *
 * @param {*} _key
 * @returns
 */
export const convertIntoIsoDate = (_key) => {
  const today = new Date().toISOString();
  const previousDate = new Date();
  switch (_key) {
    case 720:
      previousDate.setDate(previousDate.getDate() - 30);
      break;
    case 168:
      previousDate.setDate(previousDate.getDate() - 7);
      break;
    case 24:
    default:
      previousDate.setDate(previousDate.getDate() - 1);
      break;
  }
  const secondDate = new Date(previousDate).toISOString();
  return { from: secondDate, to: today };
};
/**
 * Date time formatters for calender and update event
 */
export const dateTimeFormat = {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit',
};
