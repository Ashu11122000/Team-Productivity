/* eslint-disable prettier/prettier */

import {
    Injectable,
    NotFoundException,
} from '@nestjs/common';

import {
    InjectRepository,
} from '@nestjs/typeorm';

import {
    FindOptionsWhere,
    Repository,
} from 'typeorm';

import { Notification } from '../entities/notification.entity';

import { NotificationQueryDto } from '../dto/notification-query.dto';

import { NotificationStatus } from '../../common/enums/notification-status.enum';
import { NotificationType } from '../../common/enums/notification-type.enum';

@Injectable()
export class NotificationsService {
    constructor(
        @InjectRepository(Notification)
        private readonly notificationRepository:
            Repository<Notification>,
    ) {}

    async create(params: {
        title: string;
        message: string;
        type: NotificationType;
        userId: string;
    }): Promise<Notification> {
        const notification =
            this.notificationRepository.create({
                title:
                    params.title,

                message:
                    params.message,

                type:
                    params.type,

                userId:
                    params.userId,

                status:
                    NotificationStatus.UNREAD,
            });

        return this.notificationRepository.save(
            notification,
        );
    }

    async findAll(
        query: NotificationQueryDto,
        userId: string,
    ): Promise<{
        data: Notification[];
        total: number;
        page: number;
        limit: number;
        totalPages: number;
    }> {
        const {
            page = 1,
            limit = 10,
            status,
            type,
            sortBy = 'createdAt',
            sortOrder = 'DESC',
        } = query;

        const where:
            FindOptionsWhere<Notification> =
            {
                userId,
            };

        if (status) {
            where.status = status;
        }

        if (type) {
            where.type = type;
        }

        const [data, total] =
            await this.notificationRepository.findAndCount(
                {
                    where,

                    order: {
                        [sortBy]:
                            sortOrder,
                    },

                    skip:
                        (page - 1) *
                        limit,

                    take: limit,
                },
            );

        return {
            data,
            total,
            page,
            limit,

            totalPages:
                Math.ceil(
                    total / limit,
                ),
        };
    }

    async findOne(
        id: string,
        userId: string,
    ): Promise<Notification> {
        const notification =
            await this.notificationRepository.findOne(
                {
                    where: {
                        id,
                        userId,
                    },
                },
            );

        if (!notification) {
            throw new NotFoundException(
                'Notification not found',
            );
        }

        return notification;
    }

    async markAsRead(
        id: string,
        userId: string,
    ): Promise<Notification> {
        const notification =
            await this.findOne(
                id,
                userId,
            );

        notification.status =
            NotificationStatus.READ;

        return this.notificationRepository.save(
            notification,
        );
    }

    async markAllAsRead(
        userId: string,
    ): Promise<{
        updated: number;
    }> {
        const result =
            await this.notificationRepository.update(
                {
                    userId,
                    status:
                        NotificationStatus.UNREAD,
                },
                {
                    status:
                        NotificationStatus.READ,
                },
            );

        return {
            updated:
                result.affected ?? 0,
        };
    }
}