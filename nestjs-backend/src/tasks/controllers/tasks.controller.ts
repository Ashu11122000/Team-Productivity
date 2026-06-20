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

import { TasksService } from '../services/task.service';

import { CreateTaskDto } from '../dto/create-task.dto';
import { UpdateTaskDto } from '../dto/update-task.dto';
import { TaskQueryDto } from '../dto/task-query.dto';

import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard';

import { CurrentUser } from '../../common/decorators/current-user.decorator';

import type { JwtPayload } from '../../common/interfaces/jwt-payload.interface';

import { Task } from '../entities/task.entity';

@ApiTags('Tasks')
@ApiBearerAuth('access-token')
@UseGuards(JwtAuthGuard)
@Controller('api/tasks')
export class TasksController {
    constructor(
        private readonly tasksService: TasksService,
    ) {}

    @Post()
    @ApiOperation({
        summary: 'Create Task',
    })
    @ApiResponse({
        status: 201,
        description: 'Task created successfully',
        type: Task,
    })
    async create(
        @Body()
        createTaskDto: CreateTaskDto,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<Task> {
        return this.tasksService.create(
            createTaskDto,
            user.sub,
        );
    }

    @Get()
    @ApiOperation({
        summary: 'Get User Tasks',
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
        name: 'status',
        required: false,
    })
    @ApiQuery({
        name: 'priority',
        required: false,
    })
    @ApiQuery({
        name: 'search',
        required: false,
    })
    @ApiQuery({
        name: 'sortBy',
        required: false,
    })
    @ApiQuery({
        name: 'sortOrder',
        required: false,
    })
    @ApiResponse({
        status: 200,
        description: 'Tasks retrieved successfully',
    })
    async findAll(
        @Query()
        query: TaskQueryDto,

        @CurrentUser()
        user: JwtPayload,
    ) {
        return this.tasksService.findAll(
            query,
            user.sub,
        );
    }

    @Get(':id')
    @ApiOperation({
        summary: 'Get Task By ID',
    })
    @ApiParam({
        name: 'id',
        description: 'Task UUID',
    })
    @ApiResponse({
        status: 200,
        description: 'Task retrieved successfully',
        type: Task,
    })
    async findOne(
        @Param('id')
        id: string,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<Task> {
        return this.tasksService.findOne(
            id,
            user.sub,
        );
    }

    @Patch(':id')
    @ApiOperation({
        summary: 'Update Task',
    })
    @ApiParam({
        name: 'id',
        description: 'Task UUID',
    })
    @ApiResponse({
        status: 200,
        description: 'Task updated successfully',
        type: Task,
    })
    async update(
        @Param('id')
        id: string,

        @Body()
        updateTaskDto: UpdateTaskDto,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<Task> {
        return this.tasksService.update(
            id,
            updateTaskDto,
            user.sub,
        );
    }

    @Delete(':id')
    @ApiOperation({
        summary: 'Delete Task',
    })
    @ApiParam({
        name: 'id',
        description: 'Task UUID',
    })
    @ApiResponse({
        status: 204,
        description: 'Task deleted successfully',
    })
    async remove(
        @Param('id')
        id: string,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<void> {
        return this.tasksService.remove(
            id,
            user.sub,
        );
    }
}