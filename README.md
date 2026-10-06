# Software Engineering Interview

A public, privacy-safe knowledge base for software engineering interview preparation.

This repository organizes real-world interview topics into reusable Markdown notes and an Agent Skill for structured daily practice.

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

The Markdown files preserve the useful interview questions, concepts and technical notes while removing attribution and identifying context. Source notes can be incomplete or outdated; treat them as interview prompts rather than authoritative product documentation.

## GitHub Pages

The repository includes a GitHub Pages workflow. Markdown content is rendered as a browsable static site from the `main` branch.
