package com.accenture.usermgmt.application.service;

import com.accenture.usermgmt.application.port.input.UserService;
import com.accenture.usermgmt.domain.model.User;
import com.accenture.usermgmt.domain.port.output.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

/**
 * TDD Test Suite for UserServiceImpl
 * Tests written BEFORE implementation following strict TDD principles.
 * 
 * This class tests the Application Service Layer which orchestrates:
 * - Business logic validation
 * - Duplicate detection
 * - Repository interaction
 */
@ExtendWith(MockitoExtension.class)
@DisplayName("UserServiceImpl Tests - Application Service Layer")
class UserServiceImplTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserServiceImpl userService;

    private static final String VALID_USERNAME = "john.doe";
    private static final String VALID_EMAIL = "john.doe@example.com";
    private static final Long VALID_ID = 1L;

    @BeforeEach
    void setUp() {
        // Any additional setup can go here
    }

    // ==================== CREATE USER TESTS ====================

    @Test
    @DisplayName("createUser - Success: Should save and return user when username is unique")
    void createUser_Success() {
        // ARRANGE
        // Simulate username does not exist
        when(userRepository.findByUsername(VALID_USERNAME)).thenReturn(Optional.empty());
        
        // Create expected saved user
        User savedUser = new User(VALID_ID, VALID_USERNAME, VALID_EMAIL, true);
        when(userRepository.save(any(User.class))).thenReturn(savedUser);

        // ACT
        User result = userService.createUser(VALID_USERNAME, VALID_EMAIL);

        // ASSERT
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(VALID_ID);
        assertThat(result.getUsername()).isEqualTo(VALID_USERNAME);
        assertThat(result.getEmail()).isEqualTo(VALID_EMAIL);
        assertThat(result.isActive()).isTrue();
        
        // Verify interactions
        verify(userRepository, times(1)).findByUsername(VALID_USERNAME);
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    @DisplayName("createUser - Duplicate: Should throw exception when username already exists")
    void createUser_Duplicate() {
        // ARRANGE
        // Simulate username already exists
        User existingUser = new User(VALID_ID, VALID_USERNAME, "existing@example.com", true);
        when(userRepository.findByUsername(VALID_USERNAME)).thenReturn(Optional.of(existingUser));

        // ACT & ASSERT
        assertThatThrownBy(() -> userService.createUser(VALID_USERNAME, VALID_EMAIL))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("already exists")
                .hasMessageContaining(VALID_USERNAME);
        
        // Verify save was NOT called
        verify(userRepository, times(1)).findByUsername(VALID_USERNAME);
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("createUser - Null Username: Should throw exception when username is null")
    void createUser_NullUsername() {
        // ACT & ASSERT
        assertThatThrownBy(() -> userService.createUser(null, VALID_EMAIL))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Username");
        
        // Verify repository was NOT called
        verify(userRepository, never()).findByUsername(anyString());
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("createUser - Empty Username: Should throw exception when username is empty")
    void createUser_EmptyUsername() {
        // ACT & ASSERT
        assertThatThrownBy(() -> userService.createUser("", VALID_EMAIL))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Username");
        
        // Verify repository was NOT called
        verify(userRepository, never()).findByUsername(anyString());
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("createUser - Blank Username: Should throw exception when username is blank (whitespace)")
    void createUser_BlankUsername() {
        // ACT & ASSERT
        assertThatThrownBy(() -> userService.createUser("   ", VALID_EMAIL))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Username");
        
        // Verify repository was NOT called
        verify(userRepository, never()).findByUsername(anyString());
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("createUser - Null Email: Should throw exception when email is null")
    void createUser_NullEmail() {
        // ACT & ASSERT
        assertThatThrownBy(() -> userService.createUser(VALID_USERNAME, null))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Email");
        
        // Verify repository was NOT called
        verify(userRepository, never()).findByUsername(anyString());
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("createUser - Empty Email: Should throw exception when email is empty")
    void createUser_EmptyEmail() {
        // ACT & ASSERT
        assertThatThrownBy(() -> userService.createUser(VALID_USERNAME, ""))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("Email");
        
        // Verify repository was NOT called
        verify(userRepository, never()).findByUsername(anyString());
        verify(userRepository, never()).save(any(User.class));
    }

    // ==================== GET USER TESTS ====================

    @Test
    @DisplayName("getUser - Success: Should return user when found by ID")
    void getUser_Success() {
        // ARRANGE
        User foundUser = new User(VALID_ID, VALID_USERNAME, VALID_EMAIL, true);
        when(userRepository.findById(VALID_ID)).thenReturn(Optional.of(foundUser));

        // ACT
        Optional<User> result = userService.getUser(VALID_ID);

        // ASSERT
        assertThat(result).isPresent();
        assertThat(result.get().getId()).isEqualTo(VALID_ID);
        assertThat(result.get().getUsername()).isEqualTo(VALID_USERNAME);
        assertThat(result.get().getEmail()).isEqualTo(VALID_EMAIL);
        
        verify(userRepository, times(1)).findById(VALID_ID);
    }

    @Test
    @DisplayName("getUser - Not Found: Should return empty Optional when user not found")
    void getUser_NotFound() {
        // ARRANGE
        when(userRepository.findById(VALID_ID)).thenReturn(Optional.empty());

        // ACT
        Optional<User> result = userService.getUser(VALID_ID);

        // ASSERT
        assertThat(result).isEmpty();
        
        verify(userRepository, times(1)).findById(VALID_ID);
    }

    @Test
    @DisplayName("getUser - Null ID: Should throw exception when ID is null")
    void getUser_NullId() {
        // ACT & ASSERT
        assertThatThrownBy(() -> userService.getUser(null))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("ID");
        
        // Verify repository was NOT called
        verify(userRepository, never()).findById(any());
    }

    @Test
    @DisplayName("getUser - Negative ID: Should throw exception when ID is negative")
    void getUser_NegativeId() {
        // ACT & ASSERT
        assertThatThrownBy(() -> userService.getUser(-1L))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("ID");
        
        // Verify repository was NOT called
        verify(userRepository, never()).findById(any());
    }

    @Test
    @DisplayName("getUser - Zero ID: Should throw exception when ID is zero")
    void getUser_ZeroId() {
        // ACT & ASSERT
        assertThatThrownBy(() -> userService.getUser(0L))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("ID");
        
        // Verify repository was NOT called
        verify(userRepository, never()).findById(any());
    }

    // ==================== BOUNDARY VALUE TESTS ====================

    @Test
    @DisplayName("createUser - Maximum Length Username: Should handle very long usernames")
    void createUser_MaxLengthUsername() {
        // ARRANGE
        String longUsername = "a".repeat(255); // Typical varchar(255) limit
        when(userRepository.findByUsername(longUsername)).thenReturn(Optional.empty());
        
        User savedUser = new User(VALID_ID, longUsername, VALID_EMAIL, true);
        when(userRepository.save(any(User.class))).thenReturn(savedUser);

        // ACT
        User result = userService.createUser(longUsername, VALID_EMAIL);

        // ASSERT
        assertThat(result).isNotNull();
        assertThat(result.getUsername()).hasSize(255);
        
        verify(userRepository, times(1)).findByUsername(longUsername);
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    @DisplayName("createUser - Special Characters in Username: Should handle special characters")
    void createUser_SpecialCharactersUsername() {
        // ARRANGE
        String specialUsername = "user.name-123_test";
        when(userRepository.findByUsername(specialUsername)).thenReturn(Optional.empty());
        
        User savedUser = new User(VALID_ID, specialUsername, VALID_EMAIL, true);
        when(userRepository.save(any(User.class))).thenReturn(savedUser);

        // ACT
        User result = userService.createUser(specialUsername, VALID_EMAIL);

        // ASSERT
        assertThat(result).isNotNull();
        assertThat(result.getUsername()).isEqualTo(specialUsername);
        
        verify(userRepository, times(1)).findByUsername(specialUsername);
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    @DisplayName("getUser - Maximum ID Value: Should handle Long.MAX_VALUE")
    void getUser_MaxIdValue() {
        // ARRANGE
        Long maxId = Long.MAX_VALUE;
        User foundUser = new User(maxId, VALID_USERNAME, VALID_EMAIL, true);
        when(userRepository.findById(maxId)).thenReturn(Optional.of(foundUser));

        // ACT
        Optional<User> result = userService.getUser(maxId);

        // ASSERT
        assertThat(result).isPresent();
        assertThat(result.get().getId()).isEqualTo(maxId);
        
        verify(userRepository, times(1)).findById(maxId);
    }
}
