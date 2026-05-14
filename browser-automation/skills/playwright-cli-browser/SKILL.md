---
name: playwright-cli-browser
description: Use this skill when the user wants Codex to automate browser tasks with Playwright CLI, inspect pages, generate browser scripts, take screenshots, or build repeatable web automation workflows.
metadata:
  short-description: Browser automation with Playwright CLI
---

# Playwright CLI Browser Automation

Use Playwright CLI and small Node scripts for repeatable browser tasks.

## Workflow

1. Prefer the project-local CLI: `npx playwright ...`.
2. If the workspace has no Playwright setup, install with `npm install -D playwright @playwright/test` and then `npx playwright install chromium`.
3. For quick inspection or recording, use:
   - `npx playwright codegen <url>`
   - `npx playwright open <url>`
   - `npx playwright screenshot <url> artifacts/page.png`
4. For repeatable tasks, create a focused script under `automation/` using `require('playwright')`.
5. For verification, add or run Playwright tests with `npx playwright test`.

## Implementation Rules

- Keep scripts narrow: one workflow per file.
- Save screenshots, traces, and exported data under `artifacts/`.
- Use explicit waits for stable page states instead of arbitrary sleeps.
- Prefer role, text, label, and test-id locators over brittle CSS selectors.
- Report the exact command run and the artifact path when a task creates output.

## Project Commands

When this workspace is the target:

- `npm run browser:version`
- `npm run browser:install`
- `npm run browser:visit -- <url> <screenshot-path>`
- `npm test`
