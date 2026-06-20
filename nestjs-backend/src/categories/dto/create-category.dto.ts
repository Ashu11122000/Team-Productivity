/* eslint-disable prettier/prettier */

import {
    ApiProperty,
    ApiPropertyOptional,
} from '@nestjs/swagger';

import {
    IsOptional,
    IsString,
    MaxLength,
} from 'class-validator';

export class CreateCategoryDto {
    @ApiProperty({
        example: 'Work',
    })
    @IsString()
    @MaxLength(100)
    name!: string;

    @ApiPropertyOptional({
        example: 'Tasks related to work and projects',
    })
    @IsOptional()
    @IsString()
    description?: string;

    @ApiPropertyOptional({
        example: '#3B82F6',
    })
    @IsOptional()
    @IsString()
    @MaxLength(20)
    color?: string;
}