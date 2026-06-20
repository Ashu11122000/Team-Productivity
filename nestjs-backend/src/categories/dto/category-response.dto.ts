/* eslint-disable prettier/prettier */

import { ApiProperty } from '@nestjs/swagger';

export class CategoryResponseDto {
    @ApiProperty()
    id!: string;

    @ApiProperty()
    name!: string;

    @ApiProperty({
        nullable: true,
    })
    description?: string | null;

    @ApiProperty({
        nullable: true,
    })
    color?: string | null;

    @ApiProperty()
    userId!: string;

    @ApiProperty()
    createdAt!: Date;

    @ApiProperty()
    updatedAt!: Date;
}