package com.accenture.usermgmt.infrastructure.config;

import com.accenture.usermgmt.application.port.input.UserService;
import com.accenture.usermgmt.application.service.UserServiceImpl;
import com.accenture.usermgmt.domain.port.output.UserRepository;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Spring configuration — wires the framework-free application service
 * into the Spring context by explicitly declaring it as a bean.
 */
@Configuration
public class BeanConfiguration {

    @Bean
    public UserService userService(UserRepository userRepository) {
        return new UserServiceImpl(userRepository);
    }
}
