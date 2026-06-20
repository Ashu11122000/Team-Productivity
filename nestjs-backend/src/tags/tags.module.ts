/* eslint-disable prettier/prettier */

import { Module } from '@nestjs/common';

import { TypeOrmModule } from '@nestjs/typeorm';

import { Tag } from './entities/tag.entity';

import { TagsController } from './controllers/tags.controller';

import { TagsService } from './services/tags.service';

import { ActivityLogsModule } from '../activity-logs/activity-logs.module';

@Module({
    imports: [
        TypeOrmModule.forFeature([
            Tag,
        ]),

        ActivityLogsModule,
    ],

    controllers: [
        TagsController,
    ],

    providers: [
        TagsService,
    ],

    exports: [
        TagsService,
    ],
})
export class TagsModule {}