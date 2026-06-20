/* eslint-disable prettier/prettier */

import {
    MigrationInterface,
    QueryRunner,
} from 'typeorm';

export class CreateTaskTags03
    implements MigrationInterface
{
    name = 'CreateTaskTags03';

    public async up(
        queryRunner: QueryRunner,
    ): Promise<void> {
        await queryRunner.query(`
            CREATE TABLE "task_tags" (
                "taskId"
                    uuid
                    NOT NULL,

                "tagId"
                    uuid
                    NOT NULL,

                CONSTRAINT "PK_TASK_TAGS"
                    PRIMARY KEY (
                        "taskId",
                        "tagId"
                    )
            )
        `);

        await queryRunner.query(`
            CREATE INDEX "IDX_TASK_TAG_TASK_ID"
            ON "task_tags" ("taskId")
        `);

        await queryRunner.query(`
            CREATE INDEX "IDX_TASK_TAG_TAG_ID"
            ON "task_tags" ("tagId")
        `);

        await queryRunner.query(`
            ALTER TABLE "task_tags"
            ADD CONSTRAINT "FK_TASK_TAG_TASK"
            FOREIGN KEY ("taskId")
            REFERENCES "tasks"("id")
            ON DELETE CASCADE
        `);

        await queryRunner.query(`
            ALTER TABLE "task_tags"
            ADD CONSTRAINT "FK_TASK_TAG_TAG"
            FOREIGN KEY ("tagId")
            REFERENCES "tags"("id")
            ON DELETE CASCADE
        `);
    }

    public async down(
        queryRunner: QueryRunner,
    ): Promise<void> {
        await queryRunner.query(`
            ALTER TABLE "task_tags"
            DROP CONSTRAINT "FK_TASK_TAG_TAG"
        `);

        await queryRunner.query(`
            ALTER TABLE "task_tags"
            DROP CONSTRAINT "FK_TASK_TAG_TASK"
        `);

        await queryRunner.query(`
            DROP INDEX "public"."IDX_TASK_TAG_TAG_ID"
        `);

        await queryRunner.query(`
            DROP INDEX "public"."IDX_TASK_TAG_TASK_ID"
        `);

        await queryRunner.query(`
            DROP TABLE "task_tags"
        `);
    }
}