/* eslint-disable prettier/prettier */

// This file defines a DTO for pagination queries in a NestJS application
// IsOptional is a decorator that marks a property as optional, meaning it can be omitted in the request
// Min is a decorator that validates that a number is greater than or equal to a specified minimum value
// Type is a decorator that transforms the property to a specified type, in this case, Number
import { IsOptional, Min } from 'class-validator';
import { Type } from 'class-transformer';

export class PaginationQueryDto {
  @IsOptional()
  @Type(() => Number)
  @Min(1)
  page?: number = 1;

  @IsOptional()
  @Type(() => Number)
  @Min(1)
  limit?: number = 10;
}