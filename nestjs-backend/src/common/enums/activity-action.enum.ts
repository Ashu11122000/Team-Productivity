/* eslint-disable prettier/prettier */

// This file defines an enum for activity actions in a NestJS application
export enum ActivityAction {
    TASK_CREATED = 'TASK_CREATED',
    TASK_UPDATED = 'TASK_UPDATED',
    TASK_DELETED = 'TASK_DELETED',

    CATEGORY_CREATED = 'CATEGORY_CREATED',
    CATEGORY_UPDATED = 'CATEGORY_UPDATED',
    CATEGORY_DELETED = 'CATEGORY_DELETED',

    TAG_CREATED = 'TAG_CREATED',
    TAG_UPDATED = 'TAG_UPDATED',
    TAG_DELETED = 'TAG_DELETED',
}