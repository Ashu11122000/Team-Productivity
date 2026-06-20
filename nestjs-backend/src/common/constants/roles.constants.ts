/* eslint-disable prettier/prettier */

export const ROLES = {
    ADMIN: 'ADMIN',
    USER: 'USER',
} as const;

// Role is a type that can be either 'Admin' or 'User', which are the values of the Roles object. 
// The keyof typeof Roles expression is used to get the keys of the Roles object, which are 'Admin' and 'User'
export type Role = (typeof ROLES)[keyof typeof ROLES];