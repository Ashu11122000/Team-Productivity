/* eslint-disable prettier/prettier */

import {
    Controller,
    Get,
    UseGuards,
} from '@nestjs/common';

import {
    ApiBearerAuth,
    ApiOperation,
    ApiResponse,
    ApiTags,
} from '@nestjs/swagger';

import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard';

import { CurrentUser } from '../../common/decorators/current-user.decorator';

import type { JwtPayload } from '../../common/interfaces/jwt-payload.interface';

import { AnalyticsService } from '../services/analytics.service';

import { AnalyticsOverviewDto } from '../dto/analytics-overview.dto';
import { TaskStatusStatsDto } from '../dto/task-status-stats.dto';
import { TaskPriorityStatsDto } from '../dto/task-priority.dto';
import { ProductivityStatsDto } from '../dto/productivity-stats.dto';

@ApiTags('Analytics')
@ApiBearerAuth('access-token')
@UseGuards(JwtAuthGuard)
@Controller('api/analytics')
export class AnalyticsController {
    constructor(
        private readonly analyticsService: AnalyticsService,
    ) {}

    @Get('overview')
    @ApiOperation({
        summary: 'Analytics Overview',
    })
    @ApiResponse({
        status: 200,
        type: AnalyticsOverviewDto,
    })
    async getOverview(
        @CurrentUser()
        user: JwtPayload,
    ): Promise<AnalyticsOverviewDto> {
        return this.analyticsService.getOverview(
            user.sub,
        );
    }

    @Get('tasks/status')
    @ApiOperation({
        summary: 'Task Status Statistics',
    })
    @ApiResponse({
        status: 200,
        type: TaskStatusStatsDto,
    })
    async getTaskStatusStats(
        @CurrentUser()
        user: JwtPayload,
    ): Promise<TaskStatusStatsDto> {
        return this.analyticsService.getTaskStatusStats(
            user.sub,
        );
    }

    @Get('tasks/priority')
    @ApiOperation({
        summary: 'Task Priority Statistics',
    })
    @ApiResponse({
        status: 200,
        type: TaskPriorityStatsDto,
    })
    async getTaskPriorityStats(
        @CurrentUser()
        user: JwtPayload,
    ): Promise<TaskPriorityStatsDto> {
        return this.analyticsService.getTaskPriorityStats(
            user.sub,
        );
    }

    @Get('productivity')
    @ApiOperation({
        summary: 'Productivity Statistics',
    })
    @ApiResponse({
        status: 200,
        type: ProductivityStatsDto,
    })
    async getProductivity(
        @CurrentUser()
        user: JwtPayload,
    ): Promise<ProductivityStatsDto> {
        return this.analyticsService.getProductivity(
            user.sub,
        );
    }
}