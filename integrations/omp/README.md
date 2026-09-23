# Oh My Pi (omp)

Agents converted to [omp](https://omp.sh) subagent format. Run
`./scripts/convert.sh --tool omp` to (re)generate.

## Install

From your project root (omp discovers agents from the nearest `.omp/agents/`
directory, walking upward from the current directory):

```bash
./scripts/install.sh --tool omp
```

This copies every agent to `.omp/agents/*.md` in the current directory.

## Format

Each agent becomes a single Markdown file with YAML frontmatter:

```yaml
---
name: code-reviewer
description: Reviews code for correctness, security, and maintainability.
---
```

Only `name` and `description` are required; the Markdown body is the agent's
durable instructions. The optional `tools:` frontmatter (e.g.
`tools: [read, grep, glob]`) grants an explicit read-only capability boundary;
when omitted, the agent inherits the parent session's available tools. Agency
agents are advisory personas rather than delegation-isolated workers, so
`tools` is omitted by default. Agent names are matched exactly and are
case-sensitive — prefer lowercase kebab-case names, as generated here.

## Usage

After installing, open `/agents` in omp and press `Ctrl+R` to refresh, then
ask for a specialist naturally:

```
Use the agency-frontend-developer subagent to review this component.
```

See the [subagent authoring docs](https://omp.sh/docs/subagent-authoring) for
details on tool grants, isolation, and output schemas.
