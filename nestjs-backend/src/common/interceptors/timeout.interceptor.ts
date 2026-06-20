/* eslint-disable prettier/prettier */

// RequestTimeoutException is thrown when a request takes longer than the specified timeout duration
// CallHandler is an interface that defines the handle method, which is responsible for processing the request and returning an Observable that represents the reponse
import {
  CallHandler,
  ExecutionContext,
  Injectable,
  NestInterceptor,
  RequestTimeoutException,
} from '@nestjs/common';

// Observable is a class that represents a stream of data that can be observed and manipulated
// throwError is a function that creates an Observable that emits an error notification
import { Observable, throwError } from 'rxjs';

// catchError is an operator that catches errors on the Observable stream and allows you to handle them
// timeout is an operator that throws an error if the Observable does not emit a value within the specified time frame
import {
  catchError,
  timeout,
} from 'rxjs/operators';

// NestInterceptor is an interface that defines the intercept method, which is responsible for intercepting requests and responses in a NestJS application
@Injectable()
export class TimeoutInterceptor
  implements NestInterceptor
{
  intercept(    // intercept method is called for each incoming request and allows to modify the request or response before it is sent to the client
    context: ExecutionContext,    // context is an object that provides information about the current request and response, such as request headers, parameters, and body
    next: CallHandler,        // next is an object that provides a handle method, which is responsible for processing the request and returning the Observable that represents the response
  ): Observable<unknown> {    // The intercept method returns an Observable that represents the response to be sent to the client.
    return next.handle().pipe(    // The handle method is called to process the request and returns an Observable that represents the response. The pipe method is used to apply operators to the Observable stream.
      timeout(5000),
      catchError((error) => {
        if (error.name === 'TimeoutError') {
          return throwError(
            () => new RequestTimeoutException(),
          );
        }

        return throwError(() => error);
      }),
    );
  }
}