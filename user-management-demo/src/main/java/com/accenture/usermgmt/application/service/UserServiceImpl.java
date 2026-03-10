package com.accenture.usermgmt.application.service;

import com.accenture.usermgmt.application.exception.DuplicateUsernameException;
import com.accenture.usermgmt.application.exception.InvalidUserException;
import com.accenture.usermgmt.application.port.input.CreateUserCommand;
import com.accenture.usermgmt.application.port.input.UserService;
import com.accenture.usermgmt.domain.model.User;
import com.accenture.usermgmt.domain.port.output.UserRepository;

import java.util.Optional;

/**
 * Application service — orchestrates use-cases using domain model and output ports.
 * Pure Java, no framework annotations.
 */
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public User createUser(CreateUserCommand command) {
        if (command == null) {
            throw new InvalidUserException("CreateUserCommand is required");
        }

        String username = normalizeRequired(command.username(), "Username");
        String email = normalizeRequired(command.email(), "Email");

        userRepository.findByUsername(username)
                .ifPresent(existing -> {
                    throw new DuplicateUsernameException(username);
                });

        User user = new User(null, username, email, command.active());
        return userRepository.save(user);
    }

    @Override
    public Optional<User> getUser(Long id) {
        if (id == null || id <= 0) {
            throw new InvalidUserException("ID must be a positive number");
        }
        return userRepository.findById(id);
    }

    private static String normalizeRequired(String value, String fieldName) {
        if (value == null || value.isBlank()) {
            throw new InvalidUserException(fieldName + " is required");
        }
        return value.trim();
    }
}
