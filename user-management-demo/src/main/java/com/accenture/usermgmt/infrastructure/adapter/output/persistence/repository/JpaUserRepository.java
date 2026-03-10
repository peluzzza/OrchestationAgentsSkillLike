package com.accenture.usermgmt.infrastructure.adapter.output.persistence.repository;

import com.accenture.usermgmt.infrastructure.adapter.output.persistence.entity.UserEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

/**
 * Spring Data JPA repository — framework-specific, infrastructure layer only.
 */
public interface JpaUserRepository extends JpaRepository<UserEntity, Long> {

    Optional<UserEntity> findByUsername(String username);
}
