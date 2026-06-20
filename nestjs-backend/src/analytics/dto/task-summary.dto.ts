/* eslint-disable prettier/prettier */

import { ApiProperty } from '@nestjs/swagger';

export class TaskSummaryDto {
    @ApiProperty({
        example: 120,
    })
    totalTasks!: number;

    @ApiProperty({
        example: 40,
    })
    completedTasks!: number;

    @ApiProperty({
        example: 70,
    })
    pendingTasks!: number;

    @ApiProperty({
        example: 10,
    })
    cancelledTasks!: number;

    @ApiProperty({
        example: 33.33,
    })
    completionRate!: number;
}