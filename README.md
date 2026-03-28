# Matplotlib Overlay Prototype (GSoC 2026)

This repository explores a prototype overlay system for Matplotlib, aiming to decouple dynamic interactive elements (e.g., crosshairs, tooltips) from the main figure rendering pipeline.

The goal is to investigate how localized redraw techniques (e.g., blitting) and structured overlay management can improve interactive performance and extensibility.


## Motivation

Matplotlib uses an artist-based rendering model where all elements are drawn onto a single canvas. While flexible, this approach becomes inefficient for interactive elements, as even small updates often trigger full redraws.

This project explores an alternative approach:

- Separate **static content** (plots, axes) from **dynamic overlays**
- Update only the overlay layer during interaction
- Avoid unnecessary full canvas redraws


## Core Idea

Introduce a lightweight **overlay system**:

- `OverlayElement`: independent interactive components
- `OverlayManager`: handles events, rendering, and composition
- Each overlay maintains its own state and rendering logic

This mimics a layered rendering model:
Static Figure <-- Overlay Layer(s) (Crosshair, Tooltip, Selection, ...) <-- User Interaction
