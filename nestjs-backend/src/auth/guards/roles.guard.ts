/* eslint-disable prettier/prettier */

import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';

import { Reflector } from '@nestjs/core';

import { Request } from 'express';

import { ROLES_KEY } from '../../common/decorators/roles.decorator';

import { Role } from '../../common/constants/roles.constants';

import { JwtPayload } from '../../common/interfaces/jwt-payload.interface';

interface AuthenticatedRequest extends Request {
    user: JwtPayload;
}

@Injectable()
export class RolesGuard implements CanActivate {
    constructor(
        private readonly reflector: Reflector,
    ) {}

    canActivate(
        context: ExecutionContext,
    ): boolean {
        const requiredRoles =
            this.reflector.getAllAndOverride<Role[]>(
                ROLES_KEY,
                [
                    context.getHandler(),
                    context.getClass(),
                ],
            );

        if (!requiredRoles?.length) {
            return true;
        }

        const request =
            context
                .switchToHttp()
                .getRequest<AuthenticatedRequest>();

        return requiredRoles.includes(
            request.user.role,
        );
    }
}