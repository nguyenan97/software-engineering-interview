# Software Engineering Interview

An English-first, privacy-safe knowledge base for software engineering interview preparation, with optional Vietnamese semantic notes for difficult concepts.

This repository organizes real-world interview topics into reusable Markdown notes and an Agent Skill for structured daily practice.

## Language policy

The repository is designed for an international audience while still supporting Vietnamese learners.

- **English is the primary language.**
- Technical concepts, terminology, headings, interview questions, model answers, code and diagrams stay in English.
- Established terms such as `Dependency Injection`, `Deadlock`, `Optimistic Concurrency`, `Garbage Collection`, `Idempotency` and `Eventual Consistency` are not translated into Vietnamese substitutes.
- Vietnamese is used only as optional semantic support when it helps explain meaning, intuition or a difficult mental model.
- Vietnamese notes should supplement the English content, not duplicate the full lesson.
- Interview practice is English by default.

The goal is to build both software-engineering depth and the English technical vocabulary required for real interviews and engineering discussions.

## Coverage

- C# and .NET runtime
- ASP.NET Core and API engineering
- EF Core and LINQ
- SQL Server and database performance
- Architecture and distributed systems
- Messaging and event-driven systems
- Azure and cloud architecture
- Security and identity
- Observability, performance and reliability
- DevOps, containers and delivery
- Angular, TypeScript and frontend architecture
- Coding, debugging and engineering communication

## Repository structure

```text
.
├── agent/
│   ├── SKILL.md
│   ├── TOPIC_TAXONOMY.md
│   └── LEARNING_STATE_TEMPLATE.json
├── sources/
│   ├── 01-csharp-dotnet.md
│   ├── 02-aspnet-api-ef.md
│   ├── 03-sql-data-performance.md
│   ├── 04-architecture-distributed-systems.md
│   ├── 05-security-cloud-devops.md
│   └── 06-frontend-behavioral.md
├── index.md
├── _config.yml
└── .github/workflows/pages.yml
```

## Privacy

The original notes were normalized before publication. Personal names, candidate identities, company names, project/customer names, contact details and other identifying context are intentionally excluded. The repository keeps only reusable technical/interview content.

## Source policy

The Markdown files preserve useful interview questions, concepts and technical notes while removing attribution and identifying context. Source notes can be incomplete or outdated; treat them as interview prompts rather than authoritative product documentation.

Vietnamese source questions may be normalized into natural technical English while preserving their original technical intent.

## GitHub Pages

The repository includes a GitHub Pages workflow. Markdown content is rendered as a browsable static site from the `main` branch.
