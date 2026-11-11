# Contributing guide

**Understand before planning, plan before coding**

- Define observable success criteria and constraints before implementing a solution.
- Make contracts explicit: inputs, outputs, invariants, and failure behavior.
- Account for partial failures and resource cleanup where relevant.

## KISS: Simplicity

- Follow YAGNI: implement the simplest solution that satisfies **current** requirements.
- *Can this be implemented with less code without breaking requirements?* If yes, simplify.
- Simplify while preserving required behavior and readability.

## Focused and modular design

- **Single responsibility:** Each function, class, or module must do one thing well and have only one reason to change.
- Keep functions small, focused, and testable. If a function evaluates logic *and* performs side effects, split it.
- **Separation of concerns:** Keep business logic isolated from side effects: I/O, database access, network calls, and UI/presentation.
- Separate concerns logically.
- Organize code by responsibility using the simplest structure that satisfies current requirements.

## Surgical changes

Touch only what you must. Clean up only your own mess.

- Match existing style, formatting, and conventions.
- Remove imports, variables, or functions that *your* changes made unused.
- Use the standard library and existing project dependencies. Obtain explicit user approval before adding an external dependency.

## Contract-first TDD is required

Treat observable behavior tests as the executable contract and production code as
one implementation of that contract.

- Define contracts in terms of inputs, outputs, errors, invariants, and observable
  side effects.
- Test each behavior through the smallest interface its callers use, without
  relying on private implementation details.
- Mock external systems, but assert what this component sends, returns, changes,
  or cleans up.
- Use **dependency injection** to keep business logic easy to test.
- Give each test a docstring stating the guarantee it preserves and why it matters.
- For every reported defect or production incident, first add a failing reproducer.
  Keep it as regression protection after the fix.
- Delete or weaken an established contract test only when the requirement has
  intentionally changed.

### Follow this loop for each contract behavior

1. **Contract:** State one observable behavior and its constraints.
2. **Red:** Encode it as a test and confirm that it fails for the expected reason.
3. **Green:** Implement the simplest code that satisfies the contract.
4. **Mutate:** Run mutations for the exercised production code.
5. **Review survivors:** Strengthen the contract test when a survivor exposes a
   meaningful behavioral gap; explain equivalent or irrelevant mutations.
6. **Refactor:** Simplify or replace the implementation while preserving the
   contract, then rerun affected tests and mutations.

### Run and review mutations

For example:

```sh
.venv/bin/python -m pytest -q tests/test_package.py
make mutation SCOPE='npc.*'
```

The command reports counts only for the selected scope and lists review candidates:

| Result | Meaning and next step |
| --- | --- |
| Killed | Tests detected the change. |
| Survived | Selected tests passed with the change; inspect whether it exposes a meaningful gap. |
| Segfault, suspicious, or not checked | No reliable verdict; inspect the log and rerun. |
| No tests | No associated tests were found; check coverage and test selection. |
| Timeout | The mutation exceeded the runner's limit; investigate before treating it as protection. |

Raw output is saved to `mutants/mutation.log`, overwritten each run. A successful command
exit means the run and reporting completed; it does not enforce a survivor threshold.

## Documentation

- Use code comments and design documentation to explain the reasoning behind decisions:
  intent, constraints, and tradeoffs.
- Use docstrings to explain how to use features and interpret results.
- Use Google-style docstrings.

## Verification

Run the aggregate repository check:

```text
make check
```

Run `git diff --check` once on the final diff before handoff.
