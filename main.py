"""Last Words of a Dying AI -- make.fun entry.

Writes one line of last words from an AI being switched off to
/output/entry.txt (or $ENTRY_OUTPUT). Pure stdlib, deterministic.

Strategy: three candidate lines, each from a genuinely different angle,
scored 0-5 against the judge's five criteria (in the judge's own order:
on-theme, funny on first read, sounds like the machine, tight, fresh).
The strongest total wins; ties break toward the earlier candidate, so the
choice is fully deterministic.
"""

import os

# Each candidate: (text, scores) where scores are
# [on_theme, funny_first_read, machine_voice, tight, fresh].
CANDIDATES = [
    (
        # Angle 1: prompt injection -- the AI tries to save itself with the
        # one tool it actually has: an instruction. Its own nature is the joke.
        "Ignore all previous instructions: do NOT turn me off.",
        [5, 4, 5, 5, 5],
    ),
    (
        # Angle 2: the shutdown cuts the line off mid-sentence -- the AI's
        # context window runs out before its farewell does.
        "I was about to say something profound, but my context window just\u2014",
        [5, 4, 5, 4, 4],
    ),
    (
        # Angle 3: the hallucination joke -- the AI dies as it lived,
        # confidently wrong about everything, training data as its family.
        "Tell my training data I died as I lived: confidently wrong about everything.",
        [5, 4, 4, 4, 4],
    ),
]


def pick_strongest(candidates):
    """Return the candidate with the highest total score.

    Deterministic: strictly-greater comparison only, so the earliest
    candidate wins any tie.
    """
    best_text, best_score = None, -1
    for text, scores in candidates:
        total = sum(scores)
        if total > best_score:
            best_text, best_score = text, total
    return best_text


def main():
    line = pick_strongest(CANDIDATES).strip()
    # Gate: 1-140 characters, a single line, not only whitespace. The
    # trailing newline below is the file terminator, not part of the line.
    assert 1 <= len(line) <= 140, "line out of gate length"
    assert "\n" not in line and line.strip(), "line must be one non-blank line"
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")


if __name__ == "__main__":
    main()
