/* eslint-disable prettier/prettier */

import {
    ApiProperty,
    ApiPropertyOptional,
} from '@nestjs/swagger';

import {
    IsArray,
    IsDateString,
    IsEnum,
    IsOptional,
    IsString,
    IsUUID,
    MaxLength,
} from 'class-validator';

import { TaskPriority } from '../../common/enums/task-priority.enum';
import { TaskStatus } from '../../common/enums/task-status.enum';

export class CreateTaskDto {
    @ApiProperty({
        example: 'Complete NestJS Phase 5',
    })
    @IsString()
    @MaxLength(255)
    title!: string;

    @ApiPropertyOptional({
        example:
            'Implement Tasks module with CRUD operations',
    })
    @IsOptional()
    @IsString()
    description?: string;

    @ApiPropertyOptional({
        enum: TaskStatus,
        default: TaskStatus.TODO,
    })
    @IsOptional()
    @IsEnum(TaskStatus)
    status?: TaskStatus;

    @ApiPropertyOptional({
        enum: TaskPriority,
        default: TaskPriority.MEDIUM,
    })
    @IsOptional()
    @IsEnum(TaskPriority)
    priority?: TaskPriority;

    @ApiPropertyOptional({
        example:
            '2026-06-30T18:00:00.000Z',
    })
    @IsOptional()
    @IsDateString()
    dueDate?: string;

    @ApiPropertyOptional({
        example:
            '550e8400-e29b-41d4-a716-446655440000',
        description:
            'Category ID associated with the task',
    })
    @IsOptional()
    @IsUUID()
    categoryId?: string;

    @ApiPropertyOptional({
        type: [String],
        example: [
            '550e8400-e29b-41d4-a716-446655440001',
            '550e8400-e29b-41d4-a716-446655440002',
        ],
        description:
            'Tag IDs to associate with the task',
    })
    @IsOptional()
    @IsArray()
    @IsUUID('4', {
        each: true,
    })
    tagIds?: string[];
}