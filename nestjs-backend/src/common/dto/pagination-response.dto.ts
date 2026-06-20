// This file defines a DTO for pagination responses in a NestJS application
export class PaginationResponseDto<T> {
  data!: T[];
  page!: number;
  limit!: number;
  total!: number;
  totalPages!: number;
}
