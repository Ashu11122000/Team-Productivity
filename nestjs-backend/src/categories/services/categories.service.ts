import { Injectable, NotFoundException } from '@nestjs/common';

import { InjectRepository } from '@nestjs/typeorm';

import { FindOptionsWhere, ILike, Repository } from 'typeorm';

import { Category } from '../entities/category.entity';

import { CreateCategoryDto } from '../dto/create-category.dto';
import { UpdateCategoryDto } from '../dto/update-category.dto';
import { CategoryQueryDto } from '../dto/category-query.dto';

import { ActivityLogsService } from '../../activity-logs/services/activity-logs.service';

import { NotificationsService } from '../../notifications/services/notifications.service';

import { ActivityAction } from '../../common/enums/activity-action.enum';
import { ActivityEntityType } from '../../common/enums/activity-entity-type.enum';

import { NotificationType } from '../../common/enums/notification-type.enum';

@Injectable()
export class CategoriesService {
  constructor(
    @InjectRepository(Category)
    private readonly categoryRepository: Repository<Category>,

    private readonly activityLogsService: ActivityLogsService,

    private readonly notificationsService: NotificationsService,
  ) {}

  async create(
    createCategoryDto: CreateCategoryDto,
    userId: string,
  ): Promise<Category> {
    const category = this.categoryRepository.create({
      ...createCategoryDto,
      userId,
    });

    const savedCategory = await this.categoryRepository.save(category);

    // Log activity means recording the action of creating a category in the activity logs, which can be used for auditing, tracking user actions.
    await this.activityLogsService.log({
      action: ActivityAction.CATEGORY_CREATED,

      entityType: ActivityEntityType.CATEGORY,

      entityId: savedCategory.id,

      // metadata is an object that contains additional information about the activity, such as the name and color of the created category, which can be useful for providing context in the activity logs.
      metadata: {
        name: savedCategory.name,

        color: savedCategory.color,
      },

      userId,
    });

    return savedCategory;
  }

  async findAll(
    query: CategoryQueryDto,
    userId: string,
  ): Promise<{
    data: Category[];
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

    const where: FindOptionsWhere<Category> = {
      userId,
    };

    if (search) {
      const [data, total] = await this.categoryRepository.findAndCount({
        where: [
          {
            userId,
            name: ILike(`%${search}%`),
          },
        ],

        order: {
          [sortBy]: sortOrder,
        },

        skip: (page - 1) * limit,

        take: limit,
      });

      return {
        data,
        total,
        page,
        limit,

        totalPages: Math.ceil(total / limit),
      };
    }

    const [data, total] = await this.categoryRepository.findAndCount({
      where,

      order: {
        [sortBy]: sortOrder,
      },

      skip: (page - 1) * limit,

      take: limit,
    });

    return {
      data,
      total,
      page,
      limit,

      totalPages: Math.ceil(total / limit),
    };
  }

  async findOne(id: string, userId: string): Promise<Category> {
    const category = await this.categoryRepository.findOne({
      where: {
        id,
        userId,
      },
    });

    if (!category) {
      throw new NotFoundException('Category not found');
    }

    return category;
  }

  async update(
    id: string,
    updateCategoryDto: UpdateCategoryDto,
    userId: string,
  ): Promise<Category> {
    const category = await this.findOne(id, userId);

    const previousName = category.name;

    const previousColor = category.color;

    Object.assign(category, updateCategoryDto);

    const updatedCategory = await this.categoryRepository.save(category);

    // Log notification means recording the action of updating a category in the notifications logs, which can be used for auditing, tracking user actions.
    await this.notificationsService.create({
      title: 'Category Updated',

      message: `Category "${updatedCategory.name}" was updated.`,

      type: NotificationType.CATEGORY_UPDATED,

      userId,
    });

    await this.activityLogsService.log({
      action: ActivityAction.CATEGORY_UPDATED,

      entityType: ActivityEntityType.CATEGORY,

      entityId: updatedCategory.id,

      metadata: {
        oldName: previousName,

        newName: updatedCategory.name,

        oldColor: previousColor,

        newColor: updatedCategory.color,
      },

      userId,
    });

    return updatedCategory;
  }

  async remove(id: string, userId: string): Promise<void> {
    const category = await this.findOne(id, userId);

    await this.activityLogsService.log({
      action: ActivityAction.CATEGORY_DELETED,

      entityType: ActivityEntityType.CATEGORY,

      entityId: category.id,

      metadata: {
        name: category.name,

        color: category.color,
      },

      userId,
    });

    await this.categoryRepository.remove(category);
  }
}
