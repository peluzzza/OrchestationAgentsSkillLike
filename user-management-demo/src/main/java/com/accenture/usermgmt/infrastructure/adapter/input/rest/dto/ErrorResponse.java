package com.accenture.usermgmt.infrastructure.adapter.input.rest.dto;

/**
 * Simple error payload for REST responses.
 */
public record ErrorResponse(String code, String message) {
}
