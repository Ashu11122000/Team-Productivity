/* eslint-disable prettier/prettier */

import {
    MigrationInterface,
    QueryRunner,
    Table,
    TableIndex,
} from 'typeorm';

export class CreateNotifications1719000000005
    implements MigrationInterface
{
    public async up(
        queryRunner: QueryRunner,
    ): Promise<void> {
        await queryRunner.createTable(
            new Table({
                name: 'notifications',

                columns: [
                    {
                        name: 'id',
                        type: 'uuid',
                        isPrimary: true,
                        generationStrategy:
                            'uuid',
                        default:
                            'uuid_generate_v4()',
                    },

                    {
                        name: 'title',
                        type: 'varchar',
                        length: '255',
                    },

                    {
                        name: 'message',
                        type: 'text',
                    },

                    {
                        name: 'type',
                        type: 'enum',
                        enum: [
                            'TASK_DUE',
                            'TASK_OVERDUE',
                            'TASK_COMPLETED',
                            'CATEGORY_UPDATED',
                            'TAG_ASSIGNED',
                            'SYSTEM',
                        ],
                    },

                    {
                        name: 'status',
                        type: 'enum',
                        enum: [
                            'UNREAD',
                            'READ',
                        ],
                        default:
                            `'UNREAD'`,
                    },

                    {
                        name: 'userId',
                        type: 'varchar',
                        length: '100',
                    },

                    {
                        name: 'createdAt',
                        type: 'timestamp',
                        default:
                            'CURRENT_TIMESTAMP',
                    },

                    {
                        name: 'updatedAt',
                        type: 'timestamp',
                        default:
                            'CURRENT_TIMESTAMP',
                    },
                ],
            }),
        );

        await queryRunner.createIndices(
            'notifications',
            [
                new TableIndex({
                    name:
                        'IDX_NOTIFICATION_USER_ID',
                    columnNames: [
                        'userId',
                    ],
                }),

                new TableIndex({
                    name:
                        'IDX_NOTIFICATION_STATUS',
                    columnNames: [
                        'status',
                    ],
                }),

                new TableIndex({
                    name:
                        'IDX_NOTIFICATION_TYPE',
                    columnNames: [
                        'type',
                    ],
                }),
            ],
        );
    }

    public async down(
        queryRunner: QueryRunner,
    ): Promise<void> {
        await queryRunner.dropIndex(
            'notifications',
            'IDX_NOTIFICATION_USER_ID',
        );

        await queryRunner.dropIndex(
            'notifications',
            'IDX_NOTIFICATION_STATUS',
        );

        await queryRunner.dropIndex(
            'notifications',
            'IDX_NOTIFICATION_TYPE',
        );

        await queryRunner.dropTable(
            'notifications',
        );
    }
}