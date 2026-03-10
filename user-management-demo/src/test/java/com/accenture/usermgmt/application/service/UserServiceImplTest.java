package com.accenture.usermgmt.application.service;

import com.accenture.usermgmt.application.exception.DuplicateUsernameException;
import com.accenture.usermgmt.application.port.input.CreateUserCommand;
import com.accenture.usermgmt.domain.model.User;
import com.accenture.usermgmt.domain.port.output.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceImplTest {

    @Mock
    private UserRepository userRepository;

    private UserServiceImpl userService;

    @BeforeEach
    void setUp() {
        userService = new UserServiceImpl(userRepository);
    }

    @Test
    void createUser_Success() {
        // Arrange
        CreateUserCommand command = new CreateUserCommand("jdoe", "john@example.com", true);
        User savedUser = new User(1L, "jdoe", "john@example.com", true);

        when(userRepository.findByUsername("jdoe")).thenReturn(Optional.empty());
        when(userRepository.save(any(User.class))).thenReturn(savedUser);

        // Act
        User result = userService.createUser(command);

        // Assert
        assertNotNull(result.getId());
        assertEquals("jdoe", result.getUsername());
        verify(userRepository).save(any(User.class));
    }

    @Test
    void createUser_Fail_Duplicate() {
        // Arrange
        CreateUserCommand command = new CreateUserCommand("jdoe", "john@example.com", true);
        User existingUser = new User(1L, "jdoe", "john@example.com", true);

        when(userRepository.findByUsername("jdoe")).thenReturn(Optional.of(existingUser));

        // Act & Assert
        assertThrows(DuplicateUsernameException.class, () -> userService.createUser(command));
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    void getUser_Success() {
        // Arrange
        User user = new User(1L, "jdoe", "john@example.com", true);
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));

        // Act
        Optional<User> result = userService.getUser(1L);

        // Assert
        assertTrue(result.isPresent());
        assertEquals("jdoe", result.get().getUsername());
    }

    @Test
    void getUser_NotFound() {
        // Arrange
        when(userRepository.findById(99L)).thenReturn(Optional.empty());

        // Act
        Optional<User> result = userService.getUser(99L);

        // Assert
        assertTrue(result.isEmpty());
    }
}
