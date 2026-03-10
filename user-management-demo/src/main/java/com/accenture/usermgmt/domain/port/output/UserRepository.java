package com.accenture.usermgmt.domain.port.output;

import com.accenture.usermgmt.domain.model.User;

import java.util.Optional;

/**
 * Output port — defines what the domain needs from persistence.
 * Infrastructure adapters will implement this interface.
 */
public interface UserRepository {

    User save(User user);

    Optional<User> findByUsername(String username);

    Optional<User> findById(Long id);
}
