package com.accenture.usermgmt.infrastructure.adapter.input.rest;

import com.accenture.usermgmt.application.port.input.CreateUserCommand;
import com.accenture.usermgmt.application.port.input.UserService;
import com.accenture.usermgmt.domain.model.User;
import com.accenture.usermgmt.infrastructure.adapter.input.rest.dto.CreateUserRequest;
import com.accenture.usermgmt.infrastructure.adapter.input.rest.dto.UserResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * REST adapter — driving adapter that translates HTTP requests into use-case calls.
 */
@RestController
@RequestMapping("/api/users")
public class UserRestController {

    private final UserService userService;

    public UserRestController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping
    public ResponseEntity<UserResponse> createUser(@RequestBody CreateUserRequest request) {
        boolean active = request.active() == null || request.active();
        CreateUserCommand command = new CreateUserCommand(request.username(), request.email(), active);

        User created = userService.createUser(command);
        return ResponseEntity.status(HttpStatus.CREATED).body(toResponse(created));
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        return userService.getUser(id)
                .map(user -> ResponseEntity.ok(toResponse(user)))
                .orElse(ResponseEntity.notFound().build());
    }

    private static UserResponse toResponse(User user) {
        return new UserResponse(user.getId(), user.getUsername(), user.getEmail(), user.isActive());
    }
}
