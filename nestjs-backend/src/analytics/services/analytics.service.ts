/* eslint-disable prettier/prettier */

import { Injectable } from '@nestjs/common';

import { InjectRepository } from '@nestjs/typeorm';

import { Repository } from 'typeorm';

import { Task } from '../../tasks/entities/task.entity';
import { Category } from '../../categories/entities/category.entity';
import { Tag } from '../../tags/entities/tag.entity';
import { Notification } from '../../notifications/entities/notification.entity';

import { TaskStatus } from '../../common/enums/task-status.enum';
import { TaskPriority } from '../../common/enums/task-priority.enum';

import { AnalyticsOverviewDto } from '../dto/analytics-overview.dto';
import { TaskStatusStatsDto } from '../dto/task-status-stats.dto';
import { TaskPriorityStatsDto } from '../dto/task-priority.dto';
import { ProductivityStatsDto } from '../dto/productivity-stats.dto';

@Injectable()
export class AnalyticsService {
    constructor(
        @InjectRepository(Task)
        private readonly taskRepository: Repository<Task>,

        @InjectRepository(Category)
        private readonly categoryRepository: Repository<Category>,

        @InjectRepository(Tag)
        private readonly tagRepository: Repository<Tag>,

        @InjectRepository(Notification)
        private readonly notificationRepository: Repository<Notification>,
    ) {}

    async getOverview(
        userId: string,
    ): Promise<AnalyticsOverviewDto> {
        const totalTasks =
            await this.taskRepository.count({
                where: { userId },
            });

        const completedTasks =
            await this.taskRepository.count({
                where: {
                    userId,
                    status: TaskStatus.COMPLETED,
                },
            });

        const totalCategories =
            await this.categoryRepository.count({
                where: { userId },
            });

        const totalTags =
            await this.tagRepository.count({
                where: { userId },
            });

        const totalNotifications =
            await this.notificationRepository.count({
                where: { userId },
            });

        return {
            totalTasks,
            completedTasks,
            pendingTasks:
                totalTasks - completedTasks,
            totalCategories,
            totalTags,
            totalNotifications,
        };
    }

    async getTaskStatusStats(
        userId: string,
    ): Promise<TaskStatusStatsDto> {
        return {
            todo:
                await this.taskRepository.count({
                    where: {
                        userId,
                        status: TaskStatus.TODO,
                    },
                }),

            inProgress:
                await this.taskRepository.count({
                    where: {
                        userId,
                        status:
                            TaskStatus.IN_PROGRESS,
                    },
                }),

            completed:
                await this.taskRepository.count({
                    where: {
                        userId,
                        status:
                            TaskStatus.COMPLETED,
                    },
                }),

            cancelled:
                await this.taskRepository.count({
                    where: {
                        userId,
                        status:
                            TaskStatus.CANCELLED,
                    },
                }),
        };
    }

    async getTaskPriorityStats(
        userId: string,
    ): Promise<TaskPriorityStatsDto> {
        return {
            low:
                await this.taskRepository.count({
                    where: {
                        userId,
                        priority:
                            TaskPriority.LOW,
                    },
                }),

            medium:
                await this.taskRepository.count({
                    where: {
                        userId,
                        priority:
                            TaskPriority.MEDIUM,
                    },
                }),

            high:
                await this.taskRepository.count({
                    where: {
                        userId,
                        priority:
                            TaskPriority.HIGH,
                    },
                }),

            urgent:
                await this.taskRepository.count({
                    where: {
                        userId,
                        priority:
                            TaskPriority.URGENT,
                    },
                }),
        };
    }

    async getProductivity(
        userId: string,
    ): Promise<ProductivityStatsDto> {
        const totalTasks =
            await this.taskRepository.count({
                where: { userId },
            });

        const completedTasks =
            await this.taskRepository.count({
                where: {
                    userId,
                    status: TaskStatus.COMPLETED,
                },
            });

        const activeTasks =
            totalTasks - completedTasks;

        const completionRate =
            totalTasks === 0
                ? 0
                : Number(
                    (
                        (completedTasks /
                            totalTasks) *
                        100
                    ).toFixed(2),
                );

        return {
            totalTasks,
            completedTasks,
            activeTasks,
            completionRate,
        };
    }
}