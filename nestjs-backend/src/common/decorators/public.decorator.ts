/* eslint-disable prettier/prettier */

// This file defines a custom decorator to mark routes as public in a NestJS application
// SetMetadata is a function that allows to attach metadata to a controller, which can be used later in guards or interceptors to determine if a route is public or not
import { SetMetadata } from '@nestjs/common';

// IS_PUBLIC_KEY is a constant that represents the metadata key used to mark a route as public
export const IS_PUBLIC_KEY = 'isPublic';

// Public is a custom decorator that marks a route as public by attaching the IS_PUBLIC_KEY metadata with a value of true
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);