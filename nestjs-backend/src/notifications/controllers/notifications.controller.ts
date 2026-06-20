/* eslint-disable prettier/prettier */

import {
    Controller,
    Get,
    Param,
    Patch,
    Query,
    UseGuards,
} from '@nestjs/common';

import {
    ApiBearerAuth,
    ApiOperation,
    ApiParam,
    ApiQuery,
    ApiResponse,
    ApiTags,
} from '@nestjs/swagger';

import { NotificationsService } from '../services/notifications.service';

import { NotificationQueryDto } from '../dto/notification-query.dto';

import { Notification } from '../entities/notification.entity';

import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard';

import { CurrentUser } from '../../common/decorators/current-user.decorator';

import type { JwtPayload } from '../../common/interfaces/jwt-payload.interface';

@ApiTags('Notifications')
@ApiBearerAuth('access-token')
@UseGuards(JwtAuthGuard)
@Controller('api/notifications')
export class NotificationsController {
    constructor(
        private readonly notificationsService:
            NotificationsService,
    ) {}

    @Get()
    @ApiOperation({
        summary:
            'Get User Notifications',
    })
    @ApiQuery({
        name: 'page',
        required: false,
    })
    @ApiQuery({
        name: 'limit',
        required: false,
    })
    @ApiQuery({
        name: 'status',
        required: false,
    })
    @ApiQuery({
        name: 'type',
        required: false,
    })
    @ApiQuery({
        name: 'sortBy',
        required: false,
    })
    @ApiQuery({
        name: 'sortOrder',
        required: false,
    })
    async findAll(
        @Query()
        query: NotificationQueryDto,

        @CurrentUser()
        user: JwtPayload,
    ) {
        return this.notificationsService.findAll(
            query,
            user.sub,
        );
    }

    @Get(':id')
    @ApiOperation({
        summary:
            'Get Notification By ID',
    })
    @ApiParam({
        name: 'id',
        description:
            'Notification UUID',
    })
    @ApiResponse({
        status: 200,
        type: Notification,
    })
    async findOne(
        @Param('id')
        id: string,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<Notification> {
        return this.notificationsService.findOne(
            id,
            user.sub,
        );
    }

    @Patch(':id/read')
    @ApiOperation({
        summary:
            'Mark Notification As Read',
    })
    async markAsRead(
        @Param('id')
        id: string,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<Notification> {
        return this.notificationsService.markAsRead(
            id,
            user.sub,
        );
    }

    @Patch('read-all')
    @ApiOperation({
        summary:
            'Mark All Notifications As Read',
    })
    async markAllAsRead(
        @CurrentUser()
        user: JwtPayload,
    ) {
        return this.notificationsService.markAllAsRead(
            user.sub,
        );
    }
}