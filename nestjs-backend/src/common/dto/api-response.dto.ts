// This file defines a generic DTO (Data Transfer Object) for API response in a NestJS application
// APIResponseDto is a generic class that represents the structure of an API response, including success status, message, and data
// The generic type T allows the data property to be of any type, making this DTO flexible for different API responses
export class ApiResponseDto<T> {
  success!: boolean;

  message!: string;

  data!: T;
}
