/* eslint-disable prettier/prettier */

import { ApiProperty } from '@nestjs/swagger';

export class TaskPriorityStatsDto {
    @ApiProperty()
    low!: number;

    @ApiProperty()
    medium!: number;

    @ApiProperty()
    high!: number;

    @ApiProperty()
    urgent!: number;
}