/* eslint-disable prettier/prettier */

import { Role } from '../constants/roles.constants';

export interface JwtPayload {
  sub: string;
  user_id: string;
  role: Role;
  iss: string;
  aud: string;
  iat?: number;
  exp?: number;
}