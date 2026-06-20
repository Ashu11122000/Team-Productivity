export const buildResponse = <T>(data: T, message = 'Success') => ({
  success: true,
  message,
  data,
});
