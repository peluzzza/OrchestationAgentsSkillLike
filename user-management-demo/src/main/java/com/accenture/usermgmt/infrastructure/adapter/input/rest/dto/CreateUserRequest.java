package com.accenture.usermgmt.infrastructure.adapter.input.rest.dto;

/**
 * REST request DTO for creating users.
 * Note: uses Boolean for 'active' so we can default it when omitted.
 */
public record CreateUserRequest(String username, String email, Boolean active) {
}
