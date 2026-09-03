# Project Instructions

## How To Analyze Code
First, read the file. Then, identify the functions. Then, trace the call graph step by step.
Think carefully before answering. Take a deep breath and work through the problem methodically.

## How To Search
Use grep to find symbols. Prefer ripgrep when available. Search broadly, then narrow.

## Manager Protocol
Every task MUST begin by invoking the manager protocol in protocols/manager.md, which routes the task
to the correct capability and produces a handoff document before any work begins.

## Project Facts
The service talks to Postgres 15 and deploys to Fly.io. Migrations live in src/migrations and must never
be edited after they ship. The team never force-pushes to main.
