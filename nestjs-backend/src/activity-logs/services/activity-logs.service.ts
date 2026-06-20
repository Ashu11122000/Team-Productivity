/* eslint-disable prettier/prettier */

import {
    Injectable,
    NotFoundException,
    Logger,
} from '@nestjs/common';

import {
    InjectRepository,
} from '@nestjs/typeorm';

import {
    FindOptionsWhere,
    Repository,
} from 'typeorm';

import { ActivityLog } from '../entities/activity-log.entity';

import { ActivityAction } from '../../common/enums/activity-action.enum';
import { ActivityEntityType } from '../../common/enums/activity-entity-type.enum';

import { ActivityLogQueryDto } from '../dto/activity-log-query.dto';

@Injectable()
export class ActivityLogsService {
    private readonly logger =
        new Logger(
            ActivityLogsService.name,
        );

    constructor(
        @InjectRepository(ActivityLog)
        private readonly activityLogRepository:
            Repository<ActivityLog>,
    ) {}

    async log(params: {
        action: ActivityAction;
        entityType: ActivityEntityType;
        entityId: string;
        metadata?: Record<
            string,
            unknown
        >;
        userId: string;
    }): Promise<ActivityLog> {
        try {
            this.logger.log(
                `Creating activity log`,
            );

            const activityLog =
                this.activityLogRepository.create({
                    action:
                        params.action,

                    entityType:
                        params.entityType,

                    entityId:
                        params.entityId,

                    metadata:
                        params.metadata,

                    userId:
                        params.userId,
                });

            this.logger.debug(
                JSON.stringify(
                    activityLog,
                    null,
                    2,
                ),
            );

            const savedLog =
                await this.activityLogRepository.save(
                    activityLog,
                );

            this.logger.log(
                `Activity log created: ${savedLog.id}`,
            );

            return savedLog;
        } catch (error) {
            this.logger.error(
                'Failed to create activity log',
                error instanceof Error
                    ? error.stack
                    : String(error),
            );

            throw error;
        }
    }

    async findAll(
        query: ActivityLogQueryDto,
        userId: string,
    ): Promise<{
        data: ActivityLog[];
        total: number;
        page: number;
        limit: number;
        totalPages: number;
    }> {
        const {
            page = 1,
            limit = 10,
            action,
            entityType,
            sortBy = 'createdAt',
            sortOrder = 'DESC',
        } = query;

        const where:
            FindOptionsWhere<ActivityLog> =
            {
                userId,
            };

        if (action) {
            where.action =
                action;
        }

        if (entityType) {
            where.entityType =
                entityType;
        }

        const [
            data,
            total,
        ] =
            await this.activityLogRepository.findAndCount(
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
    ): Promise<ActivityLog> {
        const activityLog =
            await this.activityLogRepository.findOne(
                {
                    where: {
                        id,
                        userId,
                    },
                },
            );

        if (!activityLog) {
            throw new NotFoundException(
                'Activity log not found',
            );
        }

        return activityLog;
    }
}