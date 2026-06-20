/* eslint-disable prettier/prettier */

import {
    Column,
    CreateDateColumn,
    Entity,
    Index,
    PrimaryGeneratedColumn,
    UpdateDateColumn,
} from 'typeorm';

import { ApiProperty } from '@nestjs/swagger';

import { NotificationType } from '../../common/enums/notification-type.enum';
import { NotificationStatus } from '../../common/enums/notification-status.enum';

@Entity({
    name: 'notifications',
})
export class Notification {
    @ApiProperty({
        example:
            '550e8400-e29b-41d4-a716-446655440000',
        description:
            'Notification unique identifier',
    })
    @PrimaryGeneratedColumn('uuid')
    id!: string;

    @ApiProperty({
        example: 'Task Due Soon',
    })
    @Column({
        type: 'varchar',
        length: 255,
    })
    title!: string;

    @ApiProperty({
        example:
            'Your task "Complete NestJS Assignment" is due soon.',
    })
    @Column({
        type: 'text',
    })
    message!: string;

    @ApiProperty({
        enum: NotificationType,
        example:
            NotificationType.TASK_DUE,
    })
    @Index(
        'IDX_NOTIFICATION_TYPE',
    )
    @Column({
        type: 'enum',
        enum: NotificationType,
    })
    type!: NotificationType;

    @ApiProperty({
        enum: NotificationStatus,
        example:
            NotificationStatus.UNREAD,
    })
    @Index(
        'IDX_NOTIFICATION_STATUS',
    )
    @Column({
        type: 'enum',
        enum: NotificationStatus,
        default:
            NotificationStatus.UNREAD,
    })
    status!: NotificationStatus;

    @ApiProperty({
        example: '1',
        description:
            'User ID from FastAPI JWT',
    })
    @Index(
        'IDX_NOTIFICATION_USER_ID',
    )
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

    @ApiProperty({
        example:
            '2026-06-13T10:30:00.000Z',
    })
    @UpdateDateColumn({
        type: 'timestamp',
    })
    updatedAt!: Date;
}