/* eslint-disable prettier/prettier */

import { ApiProperty } from '@nestjs/swagger';

import { NotificationStatus } from '../../common/enums/notification-status.enum';
import { NotificationType } from '../../common/enums/notification-type.enum';

export class NotificationResponseDto {
    @ApiProperty()
    id!: string;

    @ApiProperty()
    title!: string;

    @ApiProperty()
    message!: string;

    @ApiProperty({
        enum: NotificationType,
    })
    type!: NotificationType;

    @ApiProperty({
        enum: NotificationStatus,
    })
    status!: NotificationStatus;

    @ApiProperty()
    userId!: string;

    @ApiProperty()
    createdAt!: Date;

    @ApiProperty()
    updatedAt!: Date;
}