/* eslint-disable prettier/prettier */

import { Controller, Get, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { JwtAuthGuard } from './guards/jwt-auth.guard';

@ApiTags('Auth Test')
@Controller('auth-test')
export class AuthTestController {
    @Get('public')
    publicRoute() {
        return {
            message: 'Public Route',
        };
    }

    @ApiBearerAuth()
    @UseGuards(JwtAuthGuard)
    @Get('protected')
    protectedRoute() {
        return {
            message: 'Protected Route',
        };
    }
}