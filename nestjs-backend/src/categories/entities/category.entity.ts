/* eslint-disable prettier/prettier */

import {
    Entity,
    Column,
    CreateDateColumn,
    UpdateDateColumn,
    PrimaryGeneratedColumn,
    Index,
    OneToMany,
} from 'typeorm';

import { ApiProperty } from '@nestjs/swagger';

import { Task } from '../../tasks/entities/task.entity';

@Entity({
    name: 'categories',
})
export class Category {
    @ApiProperty({
        example: '550e8400-e29b-41d4-a716-446655440001',
        description: 'Category unique identifier',
    })
    @PrimaryGeneratedColumn('uuid')
    id!: string;

    @ApiProperty({
        example: 'Work',
        description: 'Category name',
    })
    @Column({
        type: 'varchar',
        length: 100,
    })
    name!: string;

    @ApiProperty({
        example: 'Tasks related to work and projects',
        required: false,
    })
    @Column({
        type: 'text',
        nullable: true,
    })
    description?: string | null;

    @ApiProperty({
        example: '#3B82F6',
        description: 'Category color',
        required: false,
    })
    @Column({
        type: 'varchar',
        length: 20,
        nullable: true,
    })
    color?: string | null;

    @ApiProperty({
        example: '1',
        description: 'User ID from FastAPI JWT',
    })
    @Index('IDX_CATEGORY_USER_ID')
    @Column({
        type: 'varchar',
        length: 100,
    })
    userId!: string;

    @OneToMany(
        () => Task,
        (task) => task.category,
    )
    tasks!: Task[];

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