/* eslint-disable prettier/prettier */

import { ApiProperty } from '@nestjs/swagger';

export class AnalyticsOverviewDto {
    @ApiProperty()
    totalTasks!: number;

    @ApiProperty()
    completedTasks!: number;

    @ApiProperty()
    pendingTasks!: number;

    @ApiProperty()
    totalCategories!: number;

    @ApiProperty()
    totalTags!: number;

    @ApiProperty()
    totalNotifications!: number;
}