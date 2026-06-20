import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PassportStrategy } from '@nestjs/passport';
import { JwtPayload } from '../../common/interfaces/jwt-payload.interface';

import {
  ExtractJwt,
  Strategy,
  //StrategyOptionsWithoutRequest,
} from 'passport-jwt';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy, 'jwt') {
  constructor(private readonly configService: ConfigService) {
    const secret = configService.getOrThrow<string>('jwt.secret');

    console.log('JWT SECRET =', secret);
    console.log('JWT ISSUER =', configService.get<string>('jwt.issuer'));
    console.log('JWT AUDIENCE =', configService.get<string>('jwt.audience'));

    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: secret,
      issuer: configService.get<string>('jwt.issuer'),
      audience: configService.get<string>('jwt.audience'),
      algorithms: ['HS256'],
    });
  }

  validate(payload: JwtPayload): JwtPayload {
    console.log('JWT PAYLOAD =', JSON.stringify(payload, null, 2));

    return payload;
  }
}
