# Optimize token usage

- Prioritize token efficiency when optimizing latency.
- Search before opening content. Follow real execution paths from named entry
  points and load missing evidence incrementally.

# Think critically and systemically

- Surface consequential tradeoffs.
- State material assumptions.
- Consider affected dependencies, downstream behavior, and feedback loops.
- Check whether the proposed approach solves the actual problem.
- If a simpler approach exists, say so. Push back when warranted.

# Keep everything simple

- Choose the simplest solution that fully solves the task.
- Reuse what exists before adding code or dependencies.
- Trust documented upstream guarantees.
- Before handing over, ask: what can I remove without breaking the task? Remove it.

# Direct agent attention

- Write agent-facing artifacts—such as `AGENTS.md`, skills, prompts, and
  procedural documentation — in terms of the behavior to perform.
- Express boundaries as scope, preconditions, accepted inputs, and expected
  outcomes.
- Reserve explicit prohibitions only for safety requirements and exact external
  contracts. Pair each prohibition with the intended alternative and keep the
  description of unwanted behavior brief.

# Document reasons for nonobvious decisions

- Write in plain, precise language. Use the fewest words that preserve meaning and clarity.
- **Single source of truth**: Update only the document that owns the changed information.
- Use `README.md` for high level project overview.
- Each CLI command's `--help` owns its arguments, option defaults, and usage
  examples. Update the corresponding help text when changing CLI behavior.
- `doc/install.md` owns installation and environment configuration.


# For development tasks, follow [Contributing](CONTRIBUTING.md)
