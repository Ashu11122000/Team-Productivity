/* eslint-disable prettier/prettier */

// This file defines an enum for activity entity types in a NestJS application
// ActivityEntityType is an enum that represents different types of entities that can be involved in activities, such as tasks, and categories 
export enum ActivityEntityType {
    TASK = 'TASK',
    CATEGORY = 'CATEGORY',
    TAG = 'TAG',
}