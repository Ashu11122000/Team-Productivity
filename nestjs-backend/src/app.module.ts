/* eslint-disable prettier/prettier */

import { Module } from '@nestjs/common';

import {
  ConfigModule,
  ConfigService,
} from '@nestjs/config';

import { TypeOrmModule } from '@nestjs/typeorm';

import { LoggerModule } from 'nestjs-pino';

import { configuration } from './config';

import { AuthModule } from './auth/auth.module';
import { TasksModule } from './tasks/tasks.module';
import { CategoriesModule } from './categories/categories.module';
import { TagsModule } from './tags/tags.module';
import { ActivityLogsModule } from './activity-logs/activity-logs.module';
import { NotificationsModule } from './notifications/notifications.module';
import { AnalyticsModule } from './analytics/analytics.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
      load: configuration,
    }),

    LoggerModule.forRoot({
      pinoHttp: {
        transport:
          process.env.NODE_ENV !== 'production'
            ? {
                target: 'pino-pretty',
                options: {
                  singleLine: true,
                },
              }
            : undefined,
      },
    }),

    TypeOrmModule.forRootAsync({
      inject: [ConfigService],

      useFactory: (
        configService: ConfigService,
      ) => ({
        type: 'postgres',

        host: configService.get<string>(
          'database.host',
        ),

        port: configService.get<number>(
          'database.port',
        ),

        username: configService.get<string>(
          'database.username',
        ),

        password: configService.get<string>(
          'database.password',
        ),

        database: configService.get<string>(
          'database.name',
        ),

        autoLoadEntities: true,

        synchronize: true,

        logging:
          configService.get<string>(
            'nodeEnv',
          ) === 'development',
      }),
    }),

    AuthModule,
    TasksModule,
    CategoriesModule,
    TagsModule,
    ActivityLogsModule,
    NotificationsModule,
    AnalyticsModule,
  ],
})
export class AppModule {}