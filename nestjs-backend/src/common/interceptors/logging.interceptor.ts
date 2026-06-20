/* eslint-disable prettier/prettier */

// This file defines a logging interceptor which means it will intercept the request and response cycle of the application and log the details of the request and response
// CallHandler is an interface that provides a handle() method which is called to pass control to the next interceptor or the route handler
// ExecutionContext is an interface that provides methods to access the current request and response objects 
// NestInterceptor is an interface that defines the structure of an interceptor in NestJS
import {
  CallHandler,
  ExecutionContext,
  Injectable,
  NestInterceptor,
} from '@nestjs/common';

// Observable is a class that represents a stream of data that can be observed and manipulated
import { Observable } from 'rxjs';

// tap is an operator that allows to perform side effects for notifications from the source observable
import { tap } from 'rxjs/operators';

// @Injectable() decorator marks the class as a provider that can be injected into other classes
@Injectable()
export class LoggingInterceptor implements NestInterceptor {

  // intercept method is called for each request and response cycle
  // context parameter is the ExecutionContext that provides access to the current request and response objects
  // next parameter is the CallHandler that provides a handle() method to pass control to the next interceptor or the route handler
  intercept(
    context: ExecutionContext,
    next: CallHandler,
  ): Observable<unknown> {    // switchToHttp() method is called to get the HTTP context from Execution context and getRequest() method is called to get the request object from the HTTP context
    const request = context.switchToHttp().getRequest();
    
    // Extract the HTTP method and original URL from the request object
    const { method, originalUrl } = request;

    // now variable is set to the current timestamp in milliseconds using Date.now() method
    const now = Date.now();
 
    // next.handle() method is called to pass control to the next interceptor or the route handler, and tap() operator is used to log the details of the request and response when the response is sent back to the client
    return next.handle().pipe(
      tap(() => {
        const duration = Date.now() - now;
        console.log(
          `${method} ${originalUrl} - ${duration}ms`,
        );
      }),
    );
  }
}