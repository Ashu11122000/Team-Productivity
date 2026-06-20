/* eslint-disable prettier/prettier */

import { ApiPropertyOptional } from '@nestjs/swagger';

export class MarkNotificationReadDto {
    @ApiPropertyOptional({
        example: true,
        default: true,
    })
    read?: boolean = true;
}