/* eslint-disable prettier/prettier */

import {
    Body,
    Controller,
    Delete,
    Get,
    Param,
    Patch,
    Post,
    Query,
    UseGuards,
} from '@nestjs/common';

import {
    ApiBearerAuth,
    ApiOperation,
    ApiParam,
    ApiQuery,
    ApiResponse,
    ApiTags,
} from '@nestjs/swagger';

import { CategoriesService } from '../services/categories.service';

import { Category } from '../entities/category.entity';

import { CreateCategoryDto } from '../dto/create-category.dto';
import { UpdateCategoryDto } from '../dto/update-category.dto';
import { CategoryQueryDto } from '../dto/category-query.dto';

import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard';

import { CurrentUser } from '../../common/decorators/current-user.decorator';

import type { JwtPayload } from '../../common/interfaces/jwt-payload.interface';

@ApiTags('Categories')    // ApiTags is a decorator that adds metadata to the controller, which is used by Swagger to generate API documentation.
@ApiBearerAuth('access-token')    // ApiBearerAuth is a decorator that adds metadata to the controller, which is used by Swagger to indicate that the controller requires authentication using a bearer token.
@UseGuards(JwtAuthGuard)    // useGuards is a decorator that applies the specified guards to the controller, which in this case is the JwtAuthGuard that protects the routes by requiring a valid JWT token for authentication.
@Controller('api/categories')    // Controller is a decorator that marks the class as a NestJS controller and defines the base route for all the routes in the controller, which in this case is 'api/categories'.
export class CategoriesController {
    // The constructor is used to inject the CategoriesService, which is a service that contains the business logic for handling category-related operations.
    // the CategoriesService is injected using the @Injectable decorator, which allows it to be used in the controller to perform operations such as creating, retrieving, updating, and deleting categories.
    constructor(
        private readonly categoriesService: CategoriesService,
    ) {}

    @Post()
    @ApiOperation({    // ApiOperation is a decorator that adds metadata to the route handler, which is used by Swagger to generate API documentation.
        summary: 'Create Category',
    })
    @ApiResponse({
        status: 201,
        type: Category,
    })
    async create(
        @Body()
        createCategoryDto: CreateCategoryDto,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<Category> {
        return this.categoriesService.create(
            createCategoryDto,
            user.sub,
        );
    }

    @Get()
    @ApiOperation({
        summary: 'Get User Categories',
    })
    @ApiQuery({
        name: 'page',
        required: false,
    })
    @ApiQuery({
        name: 'limit',
        required: false,
    })
    @ApiQuery({
        name: 'search',
        required: false,
    })
    async findAll(
        @Query()
        query: CategoryQueryDto,

        @CurrentUser()
        user: JwtPayload,
    ) {
        return this.categoriesService.findAll(
            query,
            user.sub,
        );
    }

    @Get(':id')
    @ApiOperation({
        summary: 'Get Category By ID',
    })
    @ApiParam({
        name: 'id',
    })
    async findOne(
        @Param('id')
        id: string,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<Category> {
        return this.categoriesService.findOne(
            id,
            user.sub,
        );
    }

    @Patch(':id')
    @ApiOperation({
        summary: 'Update Category',
    })
    @ApiResponse({
        status: 200,
        type: Category,
    })
    async update(
        @Param('id')
        id: string,

        @Body()
        updateCategoryDto: UpdateCategoryDto,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<Category> {
        return this.categoriesService.update(
            id,
            updateCategoryDto,
            user.sub,
        );
    }

    @Delete(':id')
    @ApiOperation({
        summary: 'Delete Category',
    })
    async remove(
        @Param('id')
        id: string,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<void> {
        return this.categoriesService.remove(
            id,
            user.sub,
        );
    }
}