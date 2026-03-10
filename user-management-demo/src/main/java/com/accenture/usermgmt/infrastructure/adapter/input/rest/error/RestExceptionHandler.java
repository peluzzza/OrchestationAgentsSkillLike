package com.accenture.usermgmt.infrastructure.adapter.input.rest.error;

import com.accenture.usermgmt.application.exception.DuplicateUsernameException;
import com.accenture.usermgmt.application.exception.InvalidUserException;
import com.accenture.usermgmt.infrastructure.adapter.input.rest.dto.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * Translates application-layer exceptions into HTTP responses.
 */
@RestControllerAdvice
public class RestExceptionHandler {

    @ExceptionHandler(InvalidUserException.class)
    public ResponseEntity<ErrorResponse> handleInvalidUser(InvalidUserException ex) {
        return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(new ErrorResponse("INVALID_USER", ex.getMessage()));
    }

    @ExceptionHandler(DuplicateUsernameException.class)
    public ResponseEntity<ErrorResponse> handleDuplicateUsername(DuplicateUsernameException ex) {
        return ResponseEntity.status(HttpStatus.CONFLICT)
                .body(new ErrorResponse("DUPLICATE_USERNAME", ex.getMessage()));
    }
}
