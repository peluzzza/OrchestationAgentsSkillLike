package com.accenture.usermgmt.application.port.input;

import com.accenture.usermgmt.domain.model.User;

import java.util.Optional;

/**
 * Input port — defines use-cases exposed to driving adapters (e.g. REST controllers).
 */
public interface UserService {

    User createUser(CreateUserCommand command);

    Optional<User> getUser(Long id);
}
