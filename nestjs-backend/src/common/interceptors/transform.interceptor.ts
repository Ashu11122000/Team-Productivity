/* eslint-disable prettier/prettier */

import {
  CallHandler,
  ExecutionContext,
  Injectable,
  NestInterceptor,
} from '@nestjs/common';

import { Observable } from 'rxjs';

// map is an operator that applies a given function to each value emitted by the source Observable and emits the resulting values as an Observable
import { map } from 'rxjs/operators';

@Injectable()
export class TransformInterceptor<T>    // TransformInterceptor is a generic class that implements the NestInterceptor interface.
  implements NestInterceptor<T, unknown>
{
  intercept(
    context: ExecutionContext,
    next: CallHandler,
  ): Observable<unknown> {
    return next.handle().pipe(
      map((data: any) => {    // The map operator is used to transform the data emitted by the Observable. In this case, it checks if the data us an object that contains 'data' and 'total' properties.
        if (
          data &&
          typeof data === 'object' &&    // The typeof operator is used to check if the data is an object.
          'data' in data &&    // The in operator is used to check if the data object contains the 'data' property.
          'total' in data    // The in operator is used to check if the data object contains the 'total' property.
        ) {
          return data;
        }

        return {
          success: true,
          data,
        };
      }),
    );
  }
}