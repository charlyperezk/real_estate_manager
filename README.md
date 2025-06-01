# Real Estate Manager (WIP)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/charlyperezk/real_state_manager)

This project is a real estate operation management system designed to orchestrate transactions between properties, commercial strategies, and partners, following solid software design principles.

## Status

> 🛠 In development (Work in Progress)

---

## Features

- Management of real estate operations with state tracking (`Management`, `Capture`, `Close`)
- Rich domain model using `Aggregates`, `Entities`, `Value Objects`, and `Domain Events`
- Automatic evaluation of partner performance and bonus assignment
- Proportional revenue calculation between broker and partners based on `tier` policies
- Event-driven architecture and integration with `Lato` for dependency injection and transactional execution

---

## Design principles

- **Domain-Driven Design (DDD)**: the system core is built around an expressive domain model.
- **Command Query Responsibility Segregation (CQRS)**: clear separation between write (commands) and read (queries) operations.
- **Event-Driven Architecture**: generation and publication of domain and integration events.
- **Immutability of source data**: operations do not mutate original amounts; redistributions are computed dynamically.
- **Dependency Inversion**: setup based on containers using `Dependency Injector` and `Lato`.

---

## Modules

- `operation`: logic related to the creation and update of real estate operations.
- `partner`: partner management, performance evaluation, and commission policies.
- `strategy`: tracking of commercial strategies linked to properties.
- `seedwork`: common infrastructure utilities and base contracts.