/* eslint-disable prettier/prettier */

import { ApiProperty } from '@nestjs/swagger';

export class TaskStatusStatsDto {
    @ApiProperty()
    todo!: number;

    @ApiProperty()
    inProgress!: number;

    @ApiProperty()
    completed!: number;

    @ApiProperty()
    cancelled!: number;
}