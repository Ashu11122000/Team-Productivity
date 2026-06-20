/* eslint-disable prettier/prettier */

import {
    ApiPropertyOptional,
} from '@nestjs/swagger';

import {
    IsEnum,
    IsInt,
    IsOptional,
    IsString,
    Max,
    Min,
} from 'class-validator';

import { Type } from 'class-transformer';

import { ActivityAction } from '../../common/enums/activity-action.enum';
import { ActivityEntityType } from '../../common/enums/activity-entity-type.enum';

export class ActivityLogQueryDto {
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
    @Max(100)
    limit?: number = 10;

    @ApiPropertyOptional({
        enum: ActivityAction,
    })
    @IsOptional()
    @IsEnum(ActivityAction)
    action?: ActivityAction;

    @ApiPropertyOptional({
        enum: ActivityEntityType,
    })
    @IsOptional()
    @IsEnum(ActivityEntityType)
    entityType?: ActivityEntityType;

    @ApiPropertyOptional({
        example: 'createdAt',
        default: 'createdAt',
    })
    @IsOptional()
    @IsString()
    sortBy?: string = 'createdAt';

    @ApiPropertyOptional({
        example: 'DESC',
        enum: [
            'ASC',
            'DESC',
        ],
        default: 'DESC',
    })
    @IsOptional()
    @IsString()
    sortOrder?:
        | 'ASC'
        | 'DESC' = 'DESC';
}