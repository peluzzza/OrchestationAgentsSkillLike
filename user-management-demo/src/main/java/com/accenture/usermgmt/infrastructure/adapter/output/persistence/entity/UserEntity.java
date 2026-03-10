package com.accenture.usermgmt.infrastructure.adapter.output.persistence.entity;

import jakarta.persistence.*;

/**
 * JPA entity — lives only in the infrastructure layer.
 * Mapped to/from the domain User model by the adapter.
 */
@Entity
@Table(name = "users")
public class UserEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String email;

    private boolean active;

    public UserEntity() {
    }

    public UserEntity(Long id, String username, String email, boolean active) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.active = active;
    }

    // ── Getters & Setters ──────────────────────────────────────

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }
}
