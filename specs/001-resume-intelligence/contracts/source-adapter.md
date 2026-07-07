# Contract: Source Adapter

## Purpose

Define the minimum behavior expected from a live source adapter.

## Input

- One `SourceDescriptor`
- One timeout value

## Output

- One `SourceFetchResult`

## Required Guarantees

- The adapter MUST preserve the originating source identifier.
- The adapter MUST return a status of `ok`, `unavailable`, or `empty`.
- The adapter MUST capture enough cleaned text for downstream synthesis when content is
  available.
- The adapter MUST surface fetch failures as data instead of crashing the whole run.
- The adapter MUST avoid writing secrets or private session data to repository files.

## Non-Goals for MVP

- No authenticated sessions
- No browser state persistence
- No site-specific scraping workflows that require hidden selectors or user credentials
