/* eslint-disable prettier/prettier */

// This file defines a custom decorator to mark routes with specific roles in a NestJS application
import { SetMetadata } from "@nestjs/common";
import { Role } from "../constants/roles.constants";

// ROLES_KEY is a constant that represents the metadata key used to mark a route with specific roles
export const ROLES_KEY = 'roles';

// Roles is a custom decorator that marks a route with specific roles by attaching the roles metadata with the provided roles array
export const Roles = (...roles: Role[]) => 
    SetMetadata(ROLES_KEY, roles);

