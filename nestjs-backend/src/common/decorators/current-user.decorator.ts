/* eslint-disable prettier/prettier */

// This file defines a custom decorator to extract the current user from the request object in a NestJS application
// createParamDecorator is a function that creates a custom decorator for extracting data from the request object
// ExecutionContext is an interface that provides methods to access the current request and response objects in a NestJS a
import {
  createParamDecorator,
  ExecutionContext,
} from '@nestjs/common';

// CurrentUser is a custom decorator that extracts the current user from the request object
export const CurrentUser =
  // createParamDecorator takes a function that receives the data passed to the decorator and the execution context
  createParamDecorator((_data: unknown, ctx: ExecutionContext) => {

      // switchToHttp() is a method that returns an object that allows access to the HTTP request and response objects
      // getRequest() is a method that returns the current HTTP request object
      // ctx is the execution context that provides access to the current request and response objects
      const request = ctx.switchToHttp().getRequest();

      return request.user;
    },
  );