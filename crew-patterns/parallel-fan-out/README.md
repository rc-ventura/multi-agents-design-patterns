# Parallel Fan-Out/Fan-In Pattern - CrewAI Implementation

## Overview

This implementation demonstrates the **Parallel Fan-Out/Fan-In** design pattern using CrewAI. The pattern simulates parallel code review by distributing analysis tasks across specialized agents, then synthesizing their findings into a unified Pull Request review.

## Pattern Architecture

```
                    ┌─────────────────┐
                    │   Code Input    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │  Security   │  │    Style    │  │ Performance │
    │   Auditor   │  │  Enforcer   │  │  Analyst    │
    └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
           │                │                │
           └────────────────┼────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ PR Summarizer   │
                   │  (Synthesizer)  │
                   └─────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Final Review   │
                   └─────────────────┘
```

## Agents

### 1. Security Auditor
- **Role:** Cybersecurity expert
- **Goal:** Identify vulnerabilities (SQL injection, XSS, command injection, etc.)
- **Tool:** `code_security_scanner`

### 2. Style Enforcer
- **Role:** Code style reviewer
- **Goal:** Check PEP8 compliance and formatting
- **Tool:** `style_checker`

### 3. Performance Analyst
- **Role:** Algorithms expert
- **Goal:** Analyze time/space complexity and bottlenecks
- **Tool:** `complexity_analyzer`

### 4. PR Summarizer
- **Role:** Senior technical lead
- **Goal:** Synthesize all reports into actionable PR review
- **Tool:** None (uses context from other agents)

## Tasks Flow

1. **security_audit_task** - Runs independently
2. **style_check_task** - Runs independently
3. **performance_analysis_task** - Runs independently
4. **pr_summary_task** - Synthesizes results from tasks 1-3 (via `context`)

## CrewAI Implementation Notes

### Simulated Parallelization
CrewAI uses `Process.sequential` but achieves **logical parallelization** through:
- Three independent tasks (no dependencies between them)
- One synthesis task that depends on all three via `context`

This simulates the ADK's `ParallelAgent` behavior where the three analysis tasks conceptually execute in parallel before being gathered by the summarizer.

### Comparison with ADK Google

| Aspect | ADK Google | CrewAI |
|--------|-----------|--------|
| Parallelization | `ParallelAgent` (explicit) | `Process.sequential` + `context` (logical) |
| Agent Definition | `LlmAgent` with instructions | `Agent` with YAML config |
| Orchestration | `SequentialAgent` wrapper | `Crew` with task ordering |
| Tools | Function decorators | `@tool` decorators |

## Installation

```bash
cd crew-patterns/parallel-fan-out

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and configure your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
MODEL_GEMINI=gemini/gemini-2.5-flash
GEMINI_API_KEY=your_api_key_here

OPENAI_API_KEY=your_api_key_here
MODEL_GPT=gpt-4o-mini

# Enable tracing for observability
CREWAI_TRACING_ENABLED=true
```

## Usage

**IMPORTANT:** Always activate the virtual environment first:

```bash
source .venv/bin/activate
```

### Run with Default Sample Code
```bash
# Using crewai CLI
crewai run

# Or directly via script
run_crew
```

The default sample includes intentional issues:
- Security: `eval()` usage, SQL injection risk
- Style: Nested loops, inefficient patterns
- Performance: O(n²) complexity

### Run with Custom Code

Modify `main.py` to provide your own code snippet:

```python
inputs = {"code_input": "your_code_here"}
ParallelFanOut().crew().kickoff(inputs=inputs)
```

### Other Commands

```bash
# Train the crew
train 5 training_data.pkl

# Replay a specific task
replay <task_id>

# Test the crew
test 3 gpt-4o-mini

# Run with trigger payload
run_with_trigger '{"code_input": "def foo(): pass"}'
```

## Example Output

The crew produces a comprehensive PR review with:

1. **Critical Issues** - Must fix before merge
2. **Important Improvements** - Should fix
3. **Nice-to-have Suggestions** - Optional enhancements

Each section includes:
- Security vulnerabilities with severity levels
- Style violations and PEP8 issues
- Performance bottlenecks with complexity analysis
- Actionable recommendations

## Tools

### code_security_scanner
Detects:
- `eval()`/`exec()` usage
- Command injection risks
- SQL injection patterns
- Insecure deserialization
- XSS vulnerabilities

### style_checker
Checks:
- Line length (79 chars)
- Tabs vs spaces
- Wildcard imports
- Naming conventions
- Unnecessary semicolons

### complexity_analyzer
Analyzes:
- Nested loops (O(n²) detection)
- Recursive patterns
- List operations in loops
- Conditional complexity
- Optimization opportunities

## Design Pattern Benefits

1. **Separation of Concerns:** Each agent specializes in one aspect
2. **Scalability:** Easy to add new analysis agents
3. **Comprehensive Review:** Multiple perspectives on the same code
4. **Actionable Output:** Synthesized, prioritized feedback

## Related Patterns

- **Sequential Pipeline:** Linear processing (parser → extractor → summarizer)
- **Coordinator-Dispatcher:** Dynamic routing based on intent
- **Parallel Fan-Out/Fan-In:** Multiple parallel workers → single synthesizer (this pattern)

## References

- [Google ADK Multi-Agent Patterns Guide](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- Original ADK implementation: `adk-google-patterns/parallel-fan-out/`
