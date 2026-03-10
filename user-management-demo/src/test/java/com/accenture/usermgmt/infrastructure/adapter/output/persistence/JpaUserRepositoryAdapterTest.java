package com.accenture.usermgmt.infrastructure.adapter.output.persistence;

import com.accenture.usermgmt.domain.model.User;
import com.accenture.usermgmt.infrastructure.adapter.output.persistence.entity.UserEntity;
import com.accenture.usermgmt.infrastructure.adapter.output.persistence.repository.JpaUserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class JpaUserRepositoryAdapterTest {

    @Mock
    private JpaUserRepository jpaUserRepository;

    private JpaUserRepositoryAdapter adapter;

    @BeforeEach
    void setUp() {
        adapter = new JpaUserRepositoryAdapter(jpaUserRepository);
    }

    @Test
    void save_ShouldMapDomainToEntityAndBack() {
        // Arrange
        User domainUser = new User(null, "jdoe", "john@example.com", true);

        UserEntity savedEntity = new UserEntity();
        savedEntity.setId(1L);
        savedEntity.setUsername("jdoe");
        savedEntity.setEmail("john@example.com");
        savedEntity.setActive(true);

        when(jpaUserRepository.save(any(UserEntity.class))).thenReturn(savedEntity);

        // Act
        User result = adapter.save(domainUser);

        // Assert
        assertEquals(1L, result.getId());
        assertEquals("jdoe", result.getUsername());
        assertEquals("john@example.com", result.getEmail());
        assertTrue(result.isActive());
        verify(jpaUserRepository).save(any(UserEntity.class));
    }

    @Test
    void findById_ShouldReturnMappedUser_WhenEntityExists() {
        // Arrange
        UserEntity entity = new UserEntity();
        entity.setId(1L);
        entity.setUsername("jdoe");
        entity.setEmail("john@example.com");
        entity.setActive(true);

        when(jpaUserRepository.findById(1L)).thenReturn(Optional.of(entity));

        // Act
        Optional<User> result = adapter.findById(1L);

        // Assert
        assertTrue(result.isPresent());
        assertEquals(1L, result.get().getId());
        assertEquals("jdoe", result.get().getUsername());
    }

    @Test
    void findById_ShouldReturnEmpty_WhenEntityNotFound() {
        when(jpaUserRepository.findById(99L)).thenReturn(Optional.empty());

        Optional<User> result = adapter.findById(99L);

        assertTrue(result.isEmpty());
    }

    @Test
    void findByUsername_ShouldReturnMappedUser_WhenEntityExists() {
        // Arrange
        UserEntity entity = new UserEntity();
        entity.setId(1L);
        entity.setUsername("jdoe");
        entity.setEmail("john@example.com");
        entity.setActive(true);

        when(jpaUserRepository.findByUsername("jdoe")).thenReturn(Optional.of(entity));

        // Act
        Optional<User> result = adapter.findByUsername("jdoe");

        // Assert
        assertTrue(result.isPresent());
        assertEquals("jdoe", result.get().getUsername());
    }

    @Test
    void findByUsername_ShouldReturnEmpty_WhenEntityNotFound() {
        when(jpaUserRepository.findByUsername("unknown")).thenReturn(Optional.empty());

        Optional<User> result = adapter.findByUsername("unknown");

        assertTrue(result.isEmpty());
    }
}
