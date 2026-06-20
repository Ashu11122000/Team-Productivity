/* eslint-disable prettier/prettier */

import {
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';

import { AuthGuard } from '@nestjs/passport';

@Injectable()
export class JwtAuthGuard extends AuthGuard(
  'jwt',
) {
  handleRequest(
    err: any,
    user: any,
    info: any,
  ) {
    console.log('AUTH ERROR:', err);
    console.log('AUTH INFO:', info);
    console.log('AUTH USER:', user);

    if (err || !user) {
      throw err || new UnauthorizedException();
    }

    return user;
  }
}