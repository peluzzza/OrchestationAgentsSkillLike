package com.accenture.usermgmt.application.exception;

/**
 * Thrown when input data for a use-case is invalid.
 */
public class InvalidUserException extends IllegalArgumentException {

    public InvalidUserException(String message) {
        super(message);
    }
}
