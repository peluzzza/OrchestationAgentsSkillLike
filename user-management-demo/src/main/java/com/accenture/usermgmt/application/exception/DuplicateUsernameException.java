package com.accenture.usermgmt.application.exception;

/**
 * Thrown when attempting to create a user with a username that already exists.
 */
public class DuplicateUsernameException extends RuntimeException {

    public DuplicateUsernameException(String username) {
        super("User with username '" + username + "' already exists");
    }
}
