/* eslint-disable prettier/prettier */

import { ApiProperty } from '@nestjs/swagger';

import { TaskSummaryDto } from './task-summary.dto';
import { TaskStatusStatsDto } from './task-status-stats.dto';
import { TaskPriorityStatsDto } from './task-priority.dto';

export class DashboardResponseDto {
    @ApiProperty({
        type: TaskSummaryDto,
    })
    taskSummary!: TaskSummaryDto;

    @ApiProperty({
        example: 8,
    })
    totalCategories!: number;

    @ApiProperty({
        example: 15,
    })
    totalTags!: number;

    @ApiProperty({
        example: 27,
    })
    totalNotifications!: number;

    @ApiProperty({
        type: TaskStatusStatsDto,
    })
    statusBreakdown!: TaskStatusStatsDto;

    @ApiProperty({
        type: TaskPriorityStatsDto,
    })
    priorityBreakdown!: TaskPriorityStatsDto;
}