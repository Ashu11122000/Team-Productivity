/* eslint-disable prettier/prettier */

import {
    Entity,
    Column,
    CreateDateColumn,
    UpdateDateColumn,
    PrimaryGeneratedColumn,
    Index,
    ManyToOne,
    JoinColumn,
    ManyToMany,
    JoinTable,
} from 'typeorm';

import { ApiProperty } from '@nestjs/swagger';

import { TaskStatus } from '../../common/enums/task-status.enum';
import { TaskPriority } from '../../common/enums/task-priority.enum';

import { Category } from '../../categories/entities/category.entity';
import { Tag } from '../../tags/entities/tag.entity';

@Entity({
    name: 'tasks',
})
export class Task {
    @ApiProperty({
        example: '550e8400-e29b-41d4-a716-446655440000',
        description: 'Task unique identifier',
    })
    @PrimaryGeneratedColumn('uuid')
    id!: string;

    @ApiProperty({
        example: 'Complete NestJS Assignment',
        description: 'Task title',
    })
    @Column({
        type: 'varchar',
        length: 255,
    })
    title!: string;

    @ApiProperty({
        example: 'Finish Phase 5 implementation and testing',
        description: 'Task description',
        required: false,
    })
    @Column({
        type: 'text',
        nullable: true,
    })
    description?: string | null;

    @ApiProperty({
        enum: TaskStatus,
        example: TaskStatus.TODO,
    })
    @Column({
        type: 'enum',
        enum: TaskStatus,
        default: TaskStatus.TODO,
    })
    status!: TaskStatus;

    @ApiProperty({
        enum: TaskPriority,
        example: TaskPriority.MEDIUM,
    })
    @Column({
        type: 'enum',
        enum: TaskPriority,
        default: TaskPriority.MEDIUM,
    })
    priority!: TaskPriority;

    @ApiProperty({
        example: '2026-06-20T18:00:00.000Z',
        required: false,
    })
    @Column({
        type: 'timestamp',
        nullable: true,
    })
    dueDate?: Date | null;

    @ApiProperty({
        example: '1',
        description: 'User ID from FastAPI JWT',
    })
    @Index('IDX_TASK_USER_ID')
    @Column({
        type: 'varchar',
        length: 100,
    })
    userId!: string;

    @ApiProperty({
        example: false,
        description: 'Whether task originated from note conversion',
    })
    @Column({
        type: 'boolean',
        default: false,
    })
    isConvertedFromNote!: boolean;

    @ApiProperty({
        example: '123',
        required: false,
        description: 'Original FastAPI note ID',
    })
    @Column({
        type: 'varchar',
        length: 100,
        nullable: true,
    })
    sourceNoteId?: string | null;

    @ApiProperty({
        example: '550e8400-e29b-41d4-a716-446655440001',
        required: false,
    })
    @Column({
        type: 'uuid',
        nullable: true,
    })
    categoryId?: string | null;

    @ManyToOne(
        () => Category,
        (category) => category.tasks,
        {
            nullable: true,
            onDelete: 'SET NULL',
        },
    )
    @JoinColumn({
        name: 'categoryId',
    })
    category?: Category | null;

    @ApiProperty({
        type: () => [Tag],
        required: false,
    })
    @ManyToMany(
        () => Tag,
        (tag) => tag.tasks,
    )
    @JoinTable({
        name: 'task_tags',
        joinColumn: {
            name: 'taskId',
            referencedColumnName: 'id',
        },
        inverseJoinColumn: {
            name: 'tagId',
            referencedColumnName: 'id',
        },
    })
    tags?: Tag[];

    @ApiProperty({
        example: '2026-06-13T08:00:00.000Z',
    })
    @CreateDateColumn({
        type: 'timestamp',
    })
    createdAt!: Date;

    @ApiProperty({
        example: '2026-06-13T10:30:00.000Z',
    })
    @UpdateDateColumn({
        type: 'timestamp',
    })
    updatedAt!: Date;
}