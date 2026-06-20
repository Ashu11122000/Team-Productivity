/* eslint-disable prettier/prettier */

import { Module } from '@nestjs/common';

import { TypeOrmModule } from '@nestjs/typeorm';

import { Task } from '../tasks/entities/task.entity';
import { Category } from '../categories/entities/category.entity';
import { Tag } from '../tags/entities/tag.entity';
import { Notification } from '../notifications/entities/notification.entity';

import { AnalyticsController } from './controllers/analytics.controller';

import { AnalyticsService } from './services/analytics.service';

@Module({
    imports: [
        TypeOrmModule.forFeature([
            Task,
            Category,
            Tag,
            Notification,
        ]),
    ],

    controllers: [
        AnalyticsController,
    ],

    providers: [
        AnalyticsService,
    ],
})
export class AnalyticsModule {}