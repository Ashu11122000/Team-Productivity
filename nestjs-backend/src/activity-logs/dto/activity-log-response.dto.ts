/* eslint-disable prettier/prettier */

import { ApiProperty } from '@nestjs/swagger';

import { ActivityAction } from '../../common/enums/activity-action.enum';
import { ActivityEntityType } from '../../common/enums/activity-entity-type.enum';

export class ActivityLogResponseDto {
    @ApiProperty()
    id!: string;

    @ApiProperty({
        enum: ActivityAction,
    })
    action!: ActivityAction;

    @ApiProperty({
        enum: ActivityEntityType,
    })
    entityType!: ActivityEntityType;

    @ApiProperty()
    entityId!: string;

    @ApiProperty({
        nullable: true,
        example: {
            title: 'Complete NestJS Phase 8',
        },
    })
    metadata?: Record<
        string,
        unknown
    > | null;

    @ApiProperty()
    userId!: string;

    @ApiProperty()
    createdAt!: Date;
}