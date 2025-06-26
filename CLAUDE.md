# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Language Preference

Please respond in Japanese (日本語) unless explicitly requested otherwise.

## Project Overview

This is a learning project for experimenting with Claude Code functionality. The repository serves as a sandbox for exploring Claude Code capabilities and testing various development workflows. Currently focused on developing a TODO application as a comprehensive learning exercise.

## Current Project State

### Active Project: TODO Application Development

The repository contains comprehensive planning documentation for a TODO application project:

- **Planning Phase**: Complete technical requirements and implementation roadmap in `docs/`
- **Technology Stack**: Not yet decided - will be chosen based on learning objectives
- **Architecture**: Designed to support multiple implementation approaches (frontend-only, full-stack, etc.)

### Documentation Architecture

The `docs/` folder contains the project's knowledge base:

- `todo-app-planning.md` - Technical specifications, data models, API design, security requirements
- `todo-app-implementation-plan.md` - Development phases, risk management, realistic milestones (8-week timeline)
- `learning-resources.md` - Code review checklists, ADR templates, performance guidelines

## Development Workflow

### Project Decision Process

When implementing the TODO app or starting new experiments:

1. **Technology Selection**: Refer to the decision matrix in `todo-app-planning.md` based on:
   - Learning objectives (frontend basics, full-stack experience, production-ready development)
   - Experience level (beginner, intermediate, advanced)
   - Time constraints and project scope

2. **Implementation Phases**: Follow the 7-phase approach defined in `todo-app-implementation-plan.md`:
   - Phase 1: Technology selection and environment setup (includes data model and API design)
   - Phase 2: MVP development (basic CRUD operations)
   - Phase 3-7: Progressive enhancement through UI/UX, features, testing, and deployment

3. **Quality Gates**: Each phase has defined completion criteria (Definition of Done) including:
   - Code quality checks and testing requirements
   - Security and accessibility compliance
   - Performance benchmarks and documentation updates

### Learning-Focused Development

- **ADR Documentation**: Use the template in `learning-resources.md` to record all technical decisions
- **Risk Management**: High-risk items include learning cost underestimation and scope creep
- **Iterative Approach**: 8-week timeline with 2-week phases for realistic learning progression

## Git Guidelines

- Gitのコミットメッセージは日本語で作成する
- 学習内容に応じて適切なコミット粒度を保つ
- 実験的な変更は明確にコミットメッセージで示す
- Use the code review checklist from `learning-resources.md` before committing

## Technology Readiness

The project is currently in the planning stage. Before beginning implementation:

1. Review the technology selection matrix and choose appropriate stack
2. Create project-specific subdirectory with its own README and configuration
3. Set up development environment according to chosen technology stack
4. Initialize ADR documentation for technical decisions

Future instances should prioritize completing the TODO application implementation over starting new experiments, unless explicitly requested to explore different technologies.