/* eslint-disable prettier/prettier */

import {
    MigrationInterface,
    QueryRunner,
} from 'typeorm';

export class CreateCategories01
    implements MigrationInterface
{
    name = 'CreateCategories01';

    public async up(
        queryRunner: QueryRunner,
    ): Promise<void> {
        await queryRunner.query(`
            CREATE TABLE "categories" (
                "id" uuid NOT NULL DEFAULT uuid_generate_v4(),

                "name"
                    character varying(100)
                    NOT NULL,

                "description"
                    text,

                "color"
                    character varying(20),

                "userId"
                    character varying(100)
                    NOT NULL,

                "createdAt"
                    timestamp
                    NOT NULL
                    DEFAULT now(),

                "updatedAt"
                    timestamp
                    NOT NULL
                    DEFAULT now(),

                CONSTRAINT "PK_categories_id"
                    PRIMARY KEY ("id")
            )
        `);

        await queryRunner.query(`
            CREATE INDEX "IDX_CATEGORY_USER_ID"
            ON "categories" ("userId")
        `);

        await queryRunner.query(`
            ALTER TABLE "tasks"
            ADD COLUMN "categoryId" uuid
        `);

        await queryRunner.query(`
            ALTER TABLE "tasks"
            ADD CONSTRAINT "FK_TASK_CATEGORY"
            FOREIGN KEY ("categoryId")
            REFERENCES "categories"("id")
            ON DELETE SET NULL
        `);
    }

    public async down(
        queryRunner: QueryRunner,
    ): Promise<void> {
        await queryRunner.query(`
            ALTER TABLE "tasks"
            DROP CONSTRAINT "FK_TASK_CATEGORY"
        `);

        await queryRunner.query(`
            ALTER TABLE "tasks"
            DROP COLUMN "categoryId"
        `);

        await queryRunner.query(`
            DROP INDEX "public"."IDX_CATEGORY_USER_ID"
        `);

        await queryRunner.query(`
            DROP TABLE "categories"
        `);
    }
}