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
    Repository,
} from 'typeorm';

import { Tag } from '../entities/tag.entity';

import { CreateTagDto } from '../dto/create-tag.dto';
import { UpdateTagDto } from '../dto/update-tag.dto';
import { TagQueryDto } from '../dto/tag-query.dto';

import { ActivityLogsService } from '../../activity-logs/services/activity-logs.service';

import { ActivityAction } from '../../common/enums/activity-action.enum';
import { ActivityEntityType } from '../../common/enums/activity-entity-type.enum';

@Injectable()
export class TagsService {
    constructor(
        @InjectRepository(Tag)
        private readonly tagRepository:
            Repository<Tag>,

        private readonly activityLogsService:
            ActivityLogsService,
    ) {}

    async create(
        createTagDto: CreateTagDto,
        userId: string,
    ): Promise<Tag> {
        const tag =
            this.tagRepository.create({
                ...createTagDto,
                userId,
            });

        const savedTag =
            await this.tagRepository.save(
                tag,
            );

        await this.activityLogsService.log({
            action:
                ActivityAction.TAG_CREATED,

            entityType:
                ActivityEntityType.TAG,

            entityId:
                savedTag.id,

            metadata: {
                name:
                    savedTag.name,

                color:
                    savedTag.color,
            },

            userId,
        });

        return savedTag;
    }

    async findAll(
        query: TagQueryDto,
        userId: string,
    ): Promise<{
        data: Tag[];
        total: number;
        page: number;
        limit: number;
        totalPages: number;
    }> {
        const {
            page = 1,
            limit = 10,
            search,
            sortBy = 'createdAt',
            sortOrder = 'DESC',
        } = query;

        const where:
            FindOptionsWhere<Tag> = {
                userId,
            };

        if (search) {
            const [data, total] =
                await this.tagRepository.findAndCount({
                    where: [
                        {
                            userId,
                            name: ILike(
                                `%${search}%`,
                            ),
                        },
                    ],

                    order: {
                        [sortBy]:
                            sortOrder,
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
            await this.tagRepository.findAndCount({
                where,

                order: {
                    [sortBy]:
                        sortOrder,
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

    async findOne(
        id: string,
        userId: string,
    ): Promise<Tag> {
        const tag =
            await this.tagRepository.findOne({
                where: {
                    id,
                    userId,
                },
            });

        if (!tag) {
            throw new NotFoundException(
                'Tag not found',
            );
        }

        return tag;
    }

    async update(
        id: string,
        updateTagDto: UpdateTagDto,
        userId: string,
    ): Promise<Tag> {
        const tag =
            await this.findOne(
                id,
                userId,
            );

        const previousName =
            tag.name;

        const previousColor =
            tag.color;

        Object.assign(
            tag,
            updateTagDto,
        );

        const updatedTag =
            await this.tagRepository.save(
                tag,
            );

        await this.activityLogsService.log({
            action:
                ActivityAction.TAG_UPDATED,

            entityType:
                ActivityEntityType.TAG,

            entityId:
                updatedTag.id,

            metadata: {
                oldName:
                    previousName,

                newName:
                    updatedTag.name,

                oldColor:
                    previousColor,

                newColor:
                    updatedTag.color,
            },

            userId,
        });

        return updatedTag;
    }

    async remove(
        id: string,
        userId: string,
    ): Promise<void> {
        const tag =
            await this.findOne(
                id,
                userId,
            );

        await this.activityLogsService.log({
            action:
                ActivityAction.TAG_DELETED,

            entityType:
                ActivityEntityType.TAG,

            entityId:
                tag.id,

            metadata: {
                name:
                    tag.name,

                color:
                    tag.color,
            },

            userId,
        });

        await this.tagRepository.remove(
            tag,
        );
    }
}