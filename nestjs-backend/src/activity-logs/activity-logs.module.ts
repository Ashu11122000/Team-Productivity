/* eslint-disable prettier/prettier */

import { Module } from '@nestjs/common';

import { TypeOrmModule } from '@nestjs/typeorm';

import { ActivityLog } from './entities/activity-log.entity';

import { ActivityLogsController } from './controllers/activity-logs.controller';

import { ActivityLogsService } from './services/activity-logs.service';

@Module({
    imports: [
        TypeOrmModule.forFeature([
            ActivityLog,
        ]),
    ],

    controllers: [
        ActivityLogsController,
    ],

    providers: [
        ActivityLogsService,
    ],

    exports: [
        ActivityLogsService,
    ],
})
export class ActivityLogsModule {}