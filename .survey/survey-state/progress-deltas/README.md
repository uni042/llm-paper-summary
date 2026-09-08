# Progress deltas

Small per-paper progress records used by workflow v8. Logical progress is `plan snapshot + progress delta`. Normal reading/audit runs do not rewrite the full plan or queue. Recovery deltas may reconcile an already-saved artifact, but must not double-count it.
