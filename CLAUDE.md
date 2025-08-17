# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Python Backend
- **Run the bot**: `python main.py`
- **Install dependencies**: `pip install -r requirements.txt`
- **Conda environment**: `conda env create -f environment.yml && conda activate uma`

### Web Interface (React/TypeScript)
- **Install dependencies**: `cd web && npm install`
- **Development server**: `cd web && npm run dev`
- **Build for production**: `cd web && npm run build`
- **Lint code**: `cd web && npm run lint`

## Architecture Overview

This is a computer vision automation bot for the Umamusume game with the following key components:

### Core Bot Architecture
- **main.py**: Entry point that runs FastAPI server (port 8000) and keyboard listener (F1 hotkey)
- **core/execute.py**: Main automation loop (`career_lobby()`) that handles game state detection and actions
- **core/state.py**: Game state detection using OCR - mood, turn, year, stats, failure rates
- **core/logic.py**: Training decision logic with two strategies:
  - Junior year: Train with most support cards to unlock rainbow training
  - Later years: Prioritize rainbow training (same-type support cards)
- **core/recognizer.py**: Template matching and image recognition utilities
- **core/ocr.py**: Text and number extraction from screenshots
- **utils/resolution.py**: Dynamic resolution scaling system for flexible display size support
- **utils/constants.py**: Dynamic coordinate regions that scale based on current resolution

### Configuration System
- **config.json**: Bot configuration (stat priorities, failure thresholds, auto-buy settings, display settings)
- **Resolution settings**: Auto-detect resolution, target resolution override, debug mode
- Configuration managed via web interface at `http://127.0.0.1:8000`
- Hot-reloaded on bot start via `state.reload_config()`

### Web Interface
- **React/TypeScript frontend** in `web/` directory
- **FastAPI backend** serves both API endpoints and static files
- Components for configuring training priorities, stat caps, skill auto-buy, and race preferences

### Key Game Logic
- **Training Logic**: Evaluates all 5 training types (SPD/STA/PWR/GUTS/WIT) based on support card counts and failure rates
- **Stat Caps**: Stops training stats that reach configured limits to avoid waste
- **Race Handling**: Automatically selects races with matching aptitude, prioritizes G1 races when enabled
- **Skill System**: Auto-purchases specific skills when skill points threshold is met
- **Mood Management**: Forces recreation when mood drops below threshold

### Image Assets
- **assets/buttons/**: UI buttons for navigation and actions
- **assets/icons/**: Training type and support card type icons
- **assets/ui/**: Game state indicators (G1 race, track matching, etc.)
- All image recognition uses OpenCV template matching with confidence thresholds

### Resolution Support
- **Flexible resolution support** - automatically scales to different screen sizes
- **Supported resolutions**: 1280x720, 1366x768, 1600x900, 1920x1080, 2560x1440, 3840x2160
- **Auto-detection** - automatically detects and adapts to current screen resolution
- **16:9 aspect ratio recommended** - bot works best with standard widescreen resolutions
- **Dynamic coordinate scaling** - all coordinates and regions scale proportionally

### Critical Requirements  
- **Fullscreen game required** - precise pixel-based detection
- Bot state controlled via global `state.is_bot_running` flag
- Screenshot regions defined dynamically in `utils/constants.py`

### Error Handling
- OCR misreads are common (especially failure percentages) - uses regex patterns and character replacement
- Template matching failures are handled gracefully with fallbacks to rest/recreation
- Bot automatically stops on critical errors or when game window focus is lost