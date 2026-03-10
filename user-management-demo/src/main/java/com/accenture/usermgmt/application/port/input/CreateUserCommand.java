package com.accenture.usermgmt.application.port.input;

/**
 * Command object for the "create user" use-case.
 * Keeps driving adapters decoupled from the domain model.
 */
public record CreateUserCommand(String username, String email, boolean active) {
}
