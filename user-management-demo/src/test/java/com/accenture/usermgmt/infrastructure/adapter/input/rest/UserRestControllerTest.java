package com.accenture.usermgmt.infrastructure.adapter.input.rest;

import com.accenture.usermgmt.application.port.input.CreateUserCommand;
import com.accenture.usermgmt.application.port.input.UserService;
import com.accenture.usermgmt.domain.model.User;
import com.accenture.usermgmt.infrastructure.adapter.input.rest.dto.CreateUserRequest;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Optional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserRestController.class)
class UserRestControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void createUser_ShouldReturn201() throws Exception {
        // Arrange
        CreateUserRequest inputUser = new CreateUserRequest("jdoe", "john@example.com", true);
        User savedUser = new User(1L, "jdoe", "john@example.com", true);

        when(userService.createUser(any(CreateUserCommand.class))).thenReturn(savedUser);

        // Act & Assert
        mockMvc.perform(post("/api/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(inputUser)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.username").value("jdoe"))
                .andExpect(jsonPath("$.email").value("john@example.com"))
                .andExpect(jsonPath("$.active").value(true));
    }

    @Test
    void getUser_ShouldReturn200_WhenUserExists() throws Exception {
        User user = new User(1L, "jdoe", "john@example.com", true);
        when(userService.getUser(1L)).thenReturn(Optional.of(user));

        mockMvc.perform(get("/api/users/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.username").value("jdoe"));
    }

    @Test
    void getUser_ShouldReturn404_WhenUserNotFound() throws Exception {
        when(userService.getUser(99L)).thenReturn(Optional.empty());

        mockMvc.perform(get("/api/users/99"))
                .andExpect(status().isNotFound());
    }
}
