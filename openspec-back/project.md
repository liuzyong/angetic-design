# Project Context

## Purpose
Angetic Design is a design system and component library for building consistent, accessible, and responsive user interfaces.

## Tech Stack
- TypeScript
- React
- Storybook
- Jest for testing
- CSS Modules for styling
- Figma for design

## Project Conventions

### Code Style
- Follow Airbnb JavaScript Style Guide
- Use Prettier for code formatting
- Use ESLint for linting
- Naming conventions: camelCase for variables/functions, PascalCase for components, UPPER_SNAKE_CASE for constants
- 单独的子模块需要放在src下面的子文件夹下面
- 所有的日志都放在 src/logs文件夹下面

### Architecture Patterns
- Component-based architecture
- Atomic design principles
- Reusable and composable components
- Separation of concerns between presentational and container components

### Testing Strategy
- Unit tests for all components using Jest and React Testing Library
- Visual regression testing with Storybook
- Accessibility testing
- Snapshot testing for static components

### Git Workflow
- Feature branching model
- Conventional commit messages
- Pull requests with code review required
- Squash and merge for clean history

## Domain Context
This project focuses on creating a design system that includes:
- UI components (buttons, forms, cards, etc.)
- Design tokens (colors, typography, spacing)
- Documentation and guidelines
- Accessibility standards

## Important Constraints
- Must meet WCAG 2.1 AA accessibility standards
- Support for modern browsers (Chrome, Firefox, Safari, Edge)
- Responsive design for mobile, tablet, and desktop
- Lightweight bundle size

## External Dependencies
- Figma for design collaboration
- GitHub for version control
- npm for package management
- Chromatic for visual testing
