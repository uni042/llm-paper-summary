# Discovery time-only finalization fix plan

## Goal

Align the repository canonical discovery-worker contract with the active Scheduled Chat contract: normal discovery runs may finalize only at the invocation-local handoff guard (`actual_invocation_start + 3600s`, with the 600-second guard). Discovery exhaustion, empty/duplicate rounds, round counts, candidate counts, candidate inventory, or completed Research/Audit counts must never authorize normal finalization while outside that guard.

Non-time failures remain abnormal blockers and keep their existing recovery/safe-handoff semantics.

## Scope

1. Add regression tests for `continuation_gate.py` proving that discovery exhaustion outside the handoff guard returns `CONTINUE`, while the run-deadline guard and explicit abnormal blockers still return `STOP_RUN`.
2. Change `continuation_gate.py` so discovery progression/exhaustion fields are compatibility/diagnostic inputs only and cannot create a normal stop.
3. Align `discovery-specialist-worker.md`, `discovery-exhaustive-run-policy.md`, and `discovery-continuation-policy.md` with time-only normal finalization: no minimum/maximum discovery rounds, no exhaustion stop, no minimum Research/Audit count.
4. Remove any fixed five-candidate discovery cap from canonical policy. Strong deduplicated candidates are not truncated; payloads are split only for an actual transport-size limit.
5. Run the full repository regression suite, inspect the exact discovery-gate tests, then merge only after CI is green.

## Regression cases

- Discovery, `seconds_to_run_deadline=1200`, exhaustion=true, no next axis, no independent work: `CONTINUE`, `finalization_allowed=false`, `required_action=DISCOVER_AGAIN`, and no exhaustion stop reason.
- Discovery, `seconds_to_run_deadline=600`: `STOP_RUN`, `run_deadline_within_handoff_guard`, finalization allowed.
- Discovery with canonical GitHub read unavailable: remains `STOP_RUN` as an abnormal blocker.

## Non-goals

- Do not change claim ownership, transport durability, Library fallback, or 30-second pending-result semantics.
- Do not weaken explicit abnormal blocker handling.
- Do not alter the `:30` main survey worker beyond shared canonical text that must remain semantically consistent.