<!--
SYNC IMPACT REPORT:
- Version change: N/A → 1.0.0
- Added sections: Core Principles (6 principles), Additional Constraints, Development Workflow, Governance
- Modified principles: None (new project)
- Templates requiring updates: ✅ plan-template.md, ✅ spec-template.md, ✅ tasks-template.md updated to align with new principles
- Follow-up TODOs: None
-->

# AI/Spec-Driven Book Creation using Docusaurus Constitution

## Core Principles

### I. Spec-driven development (NON-NEGOTIABLE)
All content produced through Spec-Kit Plus workflows. This ensures every feature and content piece is planned, specified, and validated before implementation, maintaining consistency and quality across the entire book project.
<!-- Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### II. Clarity and accessibility for broad technical audience
All content must be clear, concise, and technically accurate with consistent structure, tone, and terminology across the entire book. This ensures the book serves its intended audience effectively.
<!-- Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### III. Maintainability through versioned documentation
Book must be easy to update through versioned documentation. All content follows Docusaurus best practices with consistent folder structure for docs and assets, ensuring long-term project sustainability.
<!-- TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### IV. Ethical and accurate use of AI-generated content
Zero tolerance for plagiarism in AI-generated content. All external facts must be verifiable through reputable sources, ensuring the integrity and credibility of the book.
<!-- Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### V. Docusaurus Standards Compliance
Documentation structure must follow Docusaurus best practices (sidebars, versioning, markdown standards). All content must be in Markdown (.md or .mdx) format, deployed on GitHub Pages.
<!-- Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

### VI. Workflow Consistency
All chapters must be generated and refined using Spec-Kit Plus workflows (/sp.specify, /sp.plan, /sp.tasks, /sp.implement). All drafting, iteration, and code-related content must be created through Claude Code environment.
<!-- Start simple, YAGNI principles -->


## Additional Constraints
Technology stack requirements: Docusaurus framework with React, deployed on GitHub Pages. Project files must be stored in a public GitHub repository. All figures/images must be either user-created or AI-generated with allowed licensing. Book length: minimum 8–12 chapters.

## Development Workflow
Development follows the Spec-Kit Plus workflow: specification → planning → task breakdown → implementation. All content generation must pass through Claude Code environment. Each chapter must be independently testable and reviewable. Code review requirements: all content must follow Docusaurus best practices and constitutional principles. Testing gates: content must pass plagiarism checks and maintain consistency with established terminology. Deployment approval process follows GitHub Pages deployment workflow.

## Governance
This constitution supersedes all other practices in the book creation project. All pull requests and reviews must verify compliance with these principles. Amendments require documentation, team approval, and migration plan for existing content. All development must align with constitutional principles and be documented in Prompt History Records.

All PRs/reviews must verify compliance with constitutional principles; Complexity must be justified; Use CLAUDE.md for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
