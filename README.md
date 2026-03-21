# Matplotlib Overlay Prototype (GSoC 2026)
This repository contains small experiments exploring Matplotlib's event handling and redraw behavior, as preparation for the GSoC 2026 overlay layer project. The goal is to better understand the limitations of current interactive rendering and explore possible improvements.

## Goals
- Understand how Matplotlib handles user interaction events  
- Explore redraw behavior and its limitations  
- Build simple prototypes (e.g., crosshair cursor)  

## Current Experiments
- Mouse event handling (`motion_notify_event`)  
- Basic crosshair implementation  
- Observing redraw performance  

## How to run
```bash
pip install matplotlib
python prototypes/basic_crosshair.py
