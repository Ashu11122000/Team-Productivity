/* eslint-disable prettier/prettier */

import {
    Entity,
    Column,
    CreateDateColumn,
    PrimaryGeneratedColumn,
    Index,
} from 'typeorm';

import { ApiProperty } from '@nestjs/swagger';

import { ActivityAction } from '../../common/enums/activity-action.enum';
import { ActivityEntityType } from '../../common/enums/activity-entity-type.enum';

@Entity({
    name: 'activity_logs',
})
export class ActivityLog {
    @ApiProperty({
        example:
            '550e8400-e29b-41d4-a716-446655440010',
        description:
            'Activity Log unique identifier',
    })
    @PrimaryGeneratedColumn('uuid')
    id!: string;

    @ApiProperty({
        enum: ActivityAction,
        example:
            ActivityAction.TASK_CREATED,
    })
    @Index('IDX_ACTIVITY_ACTION')
    @Column({
        type: 'enum',
        enum: ActivityAction,
    })
    action!: ActivityAction;

    @ApiProperty({
        enum: ActivityEntityType,
        example:
            ActivityEntityType.TASK,
    })
    @Index('IDX_ACTIVITY_ENTITY_TYPE')
    @Column({
        type: 'enum',
        enum: ActivityEntityType,
    })
    entityType!: ActivityEntityType;

    @ApiProperty({
        example:
            '550e8400-e29b-41d4-a716-446655440001',
        description:
            'Associated entity UUID',
    })
    @Column({
        type: 'uuid',
    })
    entityId!: string;

    @ApiProperty({
        example: {
            title: 'Complete NestJS Phase 8',
        },
        required: false,
    })
    @Column({
        type: 'jsonb',
        nullable: true,
    })
    metadata?: Record<
        string,
        unknown
    > | null;

    @ApiProperty({
        example: '1',
        description:
            'User ID from FastAPI JWT',
    })
    @Index('IDX_ACTIVITY_USER_ID')
    @Column({
        type: 'varchar',
        length: 100,
    })
    userId!: string;

    @ApiProperty({
        example:
            '2026-06-13T08:00:00.000Z',
    })
    @CreateDateColumn({
        type: 'timestamp',
    })
    createdAt!: Date;
}