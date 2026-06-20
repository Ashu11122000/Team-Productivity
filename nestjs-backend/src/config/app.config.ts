/* eslint-disable prettier/prettier */

/* This file defines the application configuration
 */
export default () => ({
    nodeEnv: process.env.NODE_ENV || 'development',    // nodeEnv is used to determine the environment the application is running in

    port: parseInt(process.env.PORT || '3001', 10),    // port is used to specify the port number the application will listen on and parseInt is used to convert the string value into an integer

    frontendUrl: process.env.FRONTEND_URL || 'http://localhost:3000',    // frontendURL is used to specify the URL of the frontend application
});