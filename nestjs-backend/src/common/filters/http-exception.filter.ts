/* eslint-disable prettier/prettier */

// This file defines a custom exception filter for handling HTTP exceptions
// The ExceptionFilter interface is implemented to catch and handle exceptions thrown by the application
// Catch decorator is used to specify that this filter will handle HTTPExceptions
// ArgumentsHost is used to access the request and response objects in the context of the exception
// HttpException is the base class for all HTTP exceptions in NestJS
// HttpStatus is an enum that contains all the standard HTTP status codes
import {
  Catch,
  ExceptionFilter,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from '@nestjs/common';

// HttpExceptionFilter is a custom exception filter that catches HTTP exceptions and formats the response
// @Catch(HttpException) decorator specifies that this filter will handle exceptions of type HttpException
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {

  // catch method is called when an exception is thrown in the application
  // exception parameter is the exception that was thrown
  // host parameter is the ArgumentsHost that provides access to the request and response objects
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();    // switchToHttp() method is called to get the HTTP context from the ArgumentsHost
    const response = ctx.getResponse();    // getResponse() method is called to get the response object from the HTTP context
    const request = ctx.getRequest();    // getRequest() method is called to get the request object from the HTTP context

    // status variable is set to the HTTP status code of the exception if it is an instance of HttpException, otherwise it is set to INTERNAL_SERVER_ERROR
    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    // response.status(status).json() method is called to set the HTTP status code and send the JSON response
    response.status(status).json({
      success: false,
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message: exception.message,
    });
  }
}