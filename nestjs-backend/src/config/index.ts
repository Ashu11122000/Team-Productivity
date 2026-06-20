/* eslint-disable prettier/prettier */

// This file defines the database configuration
import appConfig from "./app.config";
import databaseConfig from "./database.config";
import jwtConfig from "./jwt.config";

// Export the configuration array and individual configurations for use in other parts of the application
export const configuration = [
    appConfig,
    databaseConfig,
    jwtConfig,
];

export {
    appConfig,
    databaseConfig,
    jwtConfig
};