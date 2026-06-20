/* eslint-disable prettier/prettier */

import {
    Controller,
    Get,
    Param,
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

import { ActivityLogsService } from '../services/activity-logs.service';

import { ActivityLog } from '../entities/activity-log.entity';

import { ActivityLogQueryDto } from '../dto/activity-log-query.dto';

import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard';

import { CurrentUser } from '../../common/decorators/current-user.decorator';

import type { JwtPayload } from '../../common/interfaces/jwt-payload.interface';

@ApiTags('Activity Logs')
@ApiBearerAuth('access-token')
@UseGuards(JwtAuthGuard)
@Controller('api/activity-logs')
export class ActivityLogsController {
    constructor(
        private readonly activityLogsService:
            ActivityLogsService,
    ) {}

    @Get()
    @ApiOperation({
        summary:
            'Get User Activity Logs',
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
        name: 'action',
        required: false,
    })
    @ApiQuery({
        name: 'entityType',
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
    @ApiResponse({
        status: 200,
        description:
            'Activity logs retrieved successfully',
    })
    async findAll(
        @Query()
        query: ActivityLogQueryDto,

        @CurrentUser()
        user: JwtPayload,
    ) {
        return this.activityLogsService.findAll(
            query,
            user.sub,
        );
    }

    @Get(':id')
    @ApiOperation({
        summary:
            'Get Activity Log By ID',
    })
    @ApiParam({
        name: 'id',
        description:
            'Activity Log UUID',
    })
    @ApiResponse({
        status: 200,
        description:
            'Activity log retrieved successfully',
        type: ActivityLog,
    })
    async findOne(
        @Param('id')
        id: string,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<ActivityLog> {
        return this.activityLogsService.findOne(
            id,
            user.sub,
        );
    }
}