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
ILike,
In,
Repository,
} from 'typeorm';

import { Task } from '../entities/task.entity';
import { Tag } from '../../tags/entities/tag.entity';

import { CreateTaskDto } from '../dto/create-task.dto';
import { UpdateTaskDto } from '../dto/update-task.dto';
import { TaskQueryDto } from '../dto/task-query.dto';

import { ActivityLogsService } from '../../activity-logs/services/activity-logs.service';

import { NotificationsService } from '../../notifications/services/notifications.service';

import { ActivityAction } from '../../common/enums/activity-action.enum';
import { ActivityEntityType } from '../../common/enums/activity-entity-type.enum';
import { TaskStatus } from '../../common/enums/task-status.enum';

import { NotificationType } from '../../common/enums/notification-type.enum';

@Injectable()
export class TasksService {
constructor(
@InjectRepository(Task)
private readonly taskRepository:
Repository<Task>,

    @InjectRepository(Tag)
    private readonly tagRepository:
        Repository<Tag>,

    private readonly activityLogsService:
        ActivityLogsService,

    private readonly notificationsService:
        NotificationsService,
) {}

async create(
    createTaskDto: CreateTaskDto,
    userId: string,
): Promise<Task> {
    const {
        tagIds,
        ...taskData
    } = createTaskDto;

    let tags: Tag[] = [];

    if (
        tagIds &&
        tagIds.length > 0
    ) {
        tags =
            await this.tagRepository.find({
                where: {
                    id: In(tagIds),
                    userId,
                },
            });
    }

    const task =
        this.taskRepository.create({
            ...taskData,

            dueDate:
                createTaskDto.dueDate
                    ? new Date(
                        createTaskDto.dueDate,
                    )
                    : null,

            userId,

            tags,
        });

    const savedTask =
        await this.taskRepository.save(
            task,
        );

    await this.activityLogsService.log({
        action:
            ActivityAction.TASK_CREATED,

        entityType:
            ActivityEntityType.TASK,

        entityId:
            savedTask.id,

        metadata: {
            title:
                savedTask.title,

            status:
                savedTask.status,

            priority:
                savedTask.priority,
        },

        userId,
    });

    return savedTask;
}

async findAll(
    query: TaskQueryDto,
    userId: string,
): Promise<{
    data: Task[];
    total: number;
    page: number;
    limit: number;
    totalPages: number;
}> {
    const {
        page = 1,
        limit = 10,
        status,
        priority,
        search,
        sortBy = 'createdAt',
        sortOrder = 'DESC',
    } = query;
    const where: FindOptionsWhere<Task> = {
        userId,
    };

    if (status) {
        where.status = status;
    }

    if (priority) {
        where.priority = priority;
    }

    if (search) {
        const [data, total] =
            await this.taskRepository.findAndCount({
                where: [
                    {
                        userId,
                        status,
                        priority,
                        title: ILike(
                            `%${search}%`,
                        ),
                    },
                ],

                relations: {
                    category: true,
                    tags: true,
                },

                order: {
                    [sortBy]: sortOrder,
                },

                skip:
                    (page - 1) *
                    limit,

                take: limit,
            });

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

    const [data, total] =
        await this.taskRepository.findAndCount({
            where,

            relations: {
                category: true,
                tags: true,
            },

            order: {
                [sortBy]: sortOrder,
            },

            skip:
                (page - 1) * limit,

            take: limit,
        });

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
): Promise<Task> {
    const task =
        await this.taskRepository.findOne({
            where: {
                id,
                userId,
            },

            relations: {
                category: true,
                tags: true,
            },
        });

    if (!task) {
        throw new NotFoundException(
            'Task not found',
        );
    }

    return task;
}

async update(
    id: string,
    updateTaskDto: UpdateTaskDto,
    userId: string,
): Promise<Task> {
    const task =
        await this.findOne(
            id,
            userId,
        );

    const {
        tagIds,
        ...taskData
    } = updateTaskDto;

    const previousStatus =
        task.status;

    const previousPriority =
        task.priority;

    Object.assign(task, {
        ...taskData,

        dueDate:
            updateTaskDto.dueDate
                ? new Date(
                    updateTaskDto.dueDate,
                )
                : task.dueDate,
    });

    let tagsAssigned = false;

    if (tagIds) {
        task.tags =
            await this.tagRepository.find({
                where: {
                    id: In(tagIds),
                    userId,
                },
            });

        tagsAssigned =
            tagIds.length > 0;
    }

    const updatedTask =
        await this.taskRepository.save(
            task,
        );

    if (
        previousStatus !==
            TaskStatus.COMPLETED &&
        updatedTask.status ===
            TaskStatus.COMPLETED
    ) {
        await this.notificationsService.create({
            title:
                'Task Completed',

            message:
                `Task "${updatedTask.title}" has been completed.`,

            type:
                NotificationType.TASK_COMPLETED,

            userId,
        });
    }

    if (tagsAssigned) {
        await this.notificationsService.create({
            title:
                'Tags Assigned',

            message:
                `Tags were assigned to task "${updatedTask.title}".`,

            type:
                NotificationType.TAG_ASSIGNED,

            userId,
        });
    }

    await this.activityLogsService.log({
        action:
            ActivityAction.TASK_UPDATED,

        entityType:
            ActivityEntityType.TASK,

        entityId:
            updatedTask.id,

        metadata: {
            title:
                updatedTask.title,

            oldStatus:
                previousStatus,

            newStatus:
                updatedTask.status,

            oldPriority:
                previousPriority,

            newPriority:
                updatedTask.priority,
        },

        userId,
    });

    return updatedTask;
}

async remove(
    id: string,
    userId: string,
): Promise<void> {
    const task =
        await this.findOne(
            id,
            userId,
        );

    await this.activityLogsService.log({
        action:
            ActivityAction.TASK_DELETED,

        entityType:
            ActivityEntityType.TASK,

        entityId:
            task.id,

        metadata: {
            title:
                task.title,

            status:
                task.status,

            priority:
                task.priority,
        },

        userId,
    });

    await this.taskRepository.remove(
        task,
    );
}

async convertNoteToTask(
    noteId: string,
    title: string,
    description: string | undefined,
    userId: string,
): Promise<Task> {
    const task =
        this.taskRepository.create({
            title,

            description,

            userId,

            isConvertedFromNote: true,

            sourceNoteId: noteId,
        });

    const savedTask =
        await this.taskRepository.save(
            task,
        );

    await this.activityLogsService.log({
        action:
            ActivityAction.TASK_CREATED,

        entityType:
            ActivityEntityType.TASK,

        entityId:
            savedTask.id,

        metadata: {
            title:
                savedTask.title,

            sourceNoteId:
                noteId,

            convertedFromNote:
                true,
        },

        userId,
    });

    return savedTask;
}

}
