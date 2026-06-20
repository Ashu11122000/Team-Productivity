/* eslint-disable prettier/prettier */

import { ApiProperty } from '@nestjs/swagger';

export class ProductivityStatsDto {
    @ApiProperty()
    totalTasks!: number;

    @ApiProperty()
    completedTasks!: number;

    @ApiProperty()
    activeTasks!: number;

    @ApiProperty()
    completionRate!: number;
}