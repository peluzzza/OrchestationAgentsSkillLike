package com.accenture.usermgmt.infrastructure.adapter.output.persistence;

import com.accenture.usermgmt.domain.model.User;
import com.accenture.usermgmt.domain.port.output.UserRepository;
import com.accenture.usermgmt.infrastructure.adapter.output.persistence.entity.UserEntity;
import com.accenture.usermgmt.infrastructure.adapter.output.persistence.repository.JpaUserRepository;
import org.springframework.stereotype.Component;

import java.util.Optional;

/**
 * Persistence adapter — implements the domain output port using Spring Data JPA.
 * Handles mapping between the domain {@link User} and the JPA {@link UserEntity}.
 */
@Component
public class JpaUserRepositoryAdapter implements UserRepository {

    private final JpaUserRepository jpaUserRepository;

    public JpaUserRepositoryAdapter(JpaUserRepository jpaUserRepository) {
        this.jpaUserRepository = jpaUserRepository;
    }

    @Override
    public User save(User user) {
        UserEntity entity = toEntity(user);
        UserEntity saved = jpaUserRepository.save(entity);
        return toDomain(saved);
    }

    @Override
    public Optional<User> findByUsername(String username) {
        return jpaUserRepository.findByUsername(username).map(this::toDomain);
    }

    @Override
    public Optional<User> findById(Long id) {
        return jpaUserRepository.findById(id).map(this::toDomain);
    }

    // ── Mapping helpers ────────────────────────────────────────

    private UserEntity toEntity(User user) {
        return new UserEntity(user.getId(), user.getUsername(), user.getEmail(), user.isActive());
    }

    private User toDomain(UserEntity entity) {
        return new User(entity.getId(), entity.getUsername(), entity.getEmail(), entity.isActive());
    }
}
