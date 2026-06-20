/* eslint-disable prettier/prettier */

// This file defines an enum for notification types in a NestJS application
export enum NotificationType {
    TASK_DUE = 'TASK_DUE',

    TASK_OVERDUE = 'TASK_OVERDUE',

    TASK_COMPLETED = 'TASK_COMPLETED',

    CATEGORY_UPDATED = 'CATEGORY_UPDATED',

    TAG_ASSIGNED = 'TAG_ASSIGNED',

    SYSTEM = 'SYSTEM',
}