"""Save a conversation to your Graphory graph (two-step flow).

Step 1: fetch the expected document schema.
Step 2: send the conversation as a Markdown document with YAML frontmatter.

    pip install graphory
    graphory login
    python save_chat_session.py
"""

from graphory import Graphory


def main() -> None:
    g = Graphory.from_config()

    # Step 1: learn the expected shape (which frontmatter fields are required,
    # how the body should look). The schema is the source of truth - read it
    # rather than guessing.
    schema = g.conversation_schema()
    print("Conversation schema:\n", schema, "\n")

    # Step 2: send the conversation. Frontmatter must include company, title,
    # summary, and who (or participants). domain: operations marks real
    # business activity; use domain: content for material you are capturing to
    # learn from. (type is optional - the server files it as a conversation.)
    document = """---
title: Strategy chat - pricing for the next cohort
summary: Tested a 30 percent price increase with a results guarantee for the next cohort; open question is whether to cap at 20 or 30.
type: conversation
company: my-company
who:
  - Dana set the next cohort pricing strategy
domain: operations
date_saved: 2026-06-02
---

We worked through pricing for the next cohort. Decided to test a 30 percent
increase paired with a results guarantee. Open question: cap the cohort at 20
or 30. Next step: draft the new offer page this week.
"""

    result = g.save_conversation(data=document)
    print("Saved:", result)


if __name__ == "__main__":
    main()
