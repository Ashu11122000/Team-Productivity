/* eslint-disable prettier/prettier */

// This file defines the Swagger configuration for the NestJS application
// INestApplication is an interface that represents a NestJS application instance 
import { INestApplication } from '@nestjs/common';

// DocumentBuilder is a class that helps to build the Swagger document configuration
// SwaggerModule is a module that provides methods to create and setup Swagger documentation for the application
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

// setupSwagger is a function that sets up Swagger documentation for the given NestJS application instance
export function setupSwagger(app: INestApplication):
    
    // void means this function does not return any value
    void {
        const config = new DocumentBuilder()
        .setTitle('Team Productivity Platform APIs')
        .setDescription('NestJS Backend APIs for Tasks, Categories, Tags, Notifications, Analytics, and Activity Logs')
        .setVersion('1.0.0')
            .addBearerAuth({
                type: 'http',
                scheme: 'bearer',
                bearerFormat: 'JWT',
                description: 'Paste FastAPI generated access token'
            },
            'access-token'
        )
        .build();

        const document = SwaggerModule.createDocument(app, config);

        SwaggerModule.setup('api/docs', app, document);
    }