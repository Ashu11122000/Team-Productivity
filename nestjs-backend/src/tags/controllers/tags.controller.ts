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

import { TagsService } from '../services/tags.service';

import { Tag } from '../entities/tag.entity';

import { CreateTagDto } from '../dto/create-tag.dto';
import { UpdateTagDto } from '../dto/update-tag.dto';
import { TagQueryDto } from '../dto/tag-query.dto';

import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard';

import { CurrentUser } from '../../common/decorators/current-user.decorator';

import type { JwtPayload } from '../../common/interfaces/jwt-payload.interface';

@ApiTags('Tags')
@ApiBearerAuth('access-token')
@UseGuards(JwtAuthGuard)
@Controller('api/tags')
export class TagsController {
    constructor(
        private readonly tagsService: TagsService,
    ) {}

    @Post()
    @ApiOperation({
        summary: 'Create Tag',
    })
    @ApiResponse({
        status: 201,
        type: Tag,
    })
    async create(
        @Body()
        createTagDto: CreateTagDto,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<Tag> {
        return this.tagsService.create(
            createTagDto,
            user.sub,
        );
    }

    @Get()
    @ApiOperation({
        summary: 'Get User Tags',
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
        query: TagQueryDto,

        @CurrentUser()
        user: JwtPayload,
    ) {
        return this.tagsService.findAll(
            query,
            user.sub,
        );
    }

    @Get(':id')
    @ApiOperation({
        summary: 'Get Tag By ID',
    })
    @ApiParam({
        name: 'id',
    })
    async findOne(
        @Param('id')
        id: string,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<Tag> {
        return this.tagsService.findOne(
            id,
            user.sub,
        );
    }

    @Patch(':id')
    @ApiOperation({
        summary: 'Update Tag',
    })
    async update(
        @Param('id')
        id: string,

        @Body()
        updateTagDto: UpdateTagDto,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<Tag> {
        return this.tagsService.update(
            id,
            updateTagDto,
            user.sub,
        );
    }

    @Delete(':id')
    @ApiOperation({
        summary: 'Delete Tag',
    })
    async remove(
        @Param('id')
        id: string,

        @CurrentUser()
        user: JwtPayload,
    ): Promise<void> {
        return this.tagsService.remove(
            id,
            user.sub,
        );
    }
}