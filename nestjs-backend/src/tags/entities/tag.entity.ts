/* eslint-disable prettier/prettier */

import {
    Entity,
    Column,
    CreateDateColumn,
    UpdateDateColumn,
    PrimaryGeneratedColumn,
    Index,
    ManyToMany,
} from 'typeorm';

import { ApiProperty } from '@nestjs/swagger';

import { Task } from '../../tasks/entities/task.entity';

@Entity({
    name: 'tags',
})
export class Tag {
    @ApiProperty({
        example:
            '550e8400-e29b-41d4-a716-446655440002',
        description: 'Tag unique identifier',
    })
    @PrimaryGeneratedColumn('uuid')
    id!: string;

    @ApiProperty({
        example: 'Backend',
        description: 'Tag name',
    })
    @Column({
        type: 'varchar',
        length: 100,
    })
    name!: string;

    @ApiProperty({
        example: '#3B82F6',
        description: 'Tag color',
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
        description:
            'User ID from FastAPI JWT',
    })
    @Index('IDX_TAG_USER_ID')
    @Column({
        type: 'varchar',
        length: 100,
    })
    userId!: string;

    @ManyToMany(
        () => Task,
        (task) => task.tags,
    )
    tasks!: Task[];

    @ApiProperty({
        example:
            '2026-06-13T08:00:00.000Z',
    })
    @CreateDateColumn({
        type: 'timestamp',
    })
    createdAt!: Date;

    @ApiProperty({
        example:
            '2026-06-13T10:30:00.000Z',
    })
    @UpdateDateColumn({
        type: 'timestamp',
    })
    updatedAt!: Date;
}