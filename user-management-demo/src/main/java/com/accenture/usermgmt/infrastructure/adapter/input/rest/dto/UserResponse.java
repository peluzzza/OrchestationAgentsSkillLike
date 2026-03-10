package com.accenture.usermgmt.infrastructure.adapter.input.rest.dto;

/**
 * REST response DTO.
 */
public record UserResponse(Long id, String username, String email, boolean active) {
}
