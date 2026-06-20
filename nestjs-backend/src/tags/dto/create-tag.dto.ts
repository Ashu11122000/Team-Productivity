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

export class CreateTagDto {
    @ApiProperty({
        example: 'Backend',
        description: 'Tag name',
    })
    @IsString()
    @MaxLength(100)
    name!: string;

    @ApiPropertyOptional({
        example: '#3B82F6',
        description: 'Tag color',
    })
    @IsOptional()
    @IsString()
    @MaxLength(20)
    color?: string;
}