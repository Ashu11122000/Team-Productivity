/* eslint-disable prettier/prettier */

import {
    IsEnum,
    IsIn,
    IsInt,
    IsOptional,
    Min,
} from 'class-validator';

import { Type } from 'class-transformer';

import { ApiPropertyOptional } from '@nestjs/swagger';

import { NotificationStatus } from '../../common/enums/notification-status.enum';
import { NotificationType } from '../../common/enums/notification-type.enum';

export class NotificationQueryDto {
    @ApiPropertyOptional({
        example: 1,
        default: 1,
    })
    @IsOptional()
    @Type(() => Number)
    @IsInt()
    @Min(1)
    page?: number = 1;

    @ApiPropertyOptional({
        example: 10,
        default: 10,
    })
    @IsOptional()
    @Type(() => Number)
    @IsInt()
    @Min(1)
    limit?: number = 10;

    @ApiPropertyOptional({
        enum: NotificationStatus,
    })
    @IsOptional()
    @IsEnum(NotificationStatus)
    status?: NotificationStatus;

    @ApiPropertyOptional({
        enum: NotificationType,
    })
    @IsOptional()
    @IsEnum(NotificationType)
    type?: NotificationType;

    @ApiPropertyOptional({
        example: 'createdAt',
        default: 'createdAt',
    })
    @IsOptional()
    @IsIn([
        'title',
        'type',
        'status',
        'createdAt',
        'updatedAt',
    ])
    sortBy?: string = 'createdAt';

    @ApiPropertyOptional({
        example: 'DESC',
        default: 'DESC',
    })
    @IsOptional()
    @IsIn([
        'ASC',
        'DESC',
    ])
    sortOrder?: 'ASC' | 'DESC' =
        'DESC';
}