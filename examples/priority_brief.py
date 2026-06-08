"""A cron-ready daily priority brief from your Graphory graph.

Graphory provides the data; your own AI does the ranking. This script pulls the
raw signal (recent activity, graph size, open follow-ups) and prints it. Pipe
the output to your AI of choice - or extend `summarize()` to call your model -
to turn it into a ranked "what matters today" brief, a spreadsheet row, or an
email.

    pip install graphory
    graphory login
    python priority_brief.py
"""

from graphory import Graphory


def gather() -> dict:
    g = Graphory.from_config()
    return {
        "stats": g.stats(),
        "recent": g.timeline(days=7, limit=50),
        "open_threads": g.search("follow up deadline project unpaid", limit=25),
    }


def summarize(data: dict) -> str:
    """Replace this with a call to your own AI to rank and phrase the brief.

    Graphory does not run an LLM for you - bring your own. The data gathered
    above is everything your model needs to write a useful brief.
    """
    lines = [f"Graph: {data['stats'].get('total_nodes', 0)} items"]
    lines.append(f"Recent activity (7d): {len(data['recent'])} events")
    for ev in data["recent"][:10]:
        when = ev.get("occurred_at", "")
        name = ev.get("name", ev.get("id", ""))
        lines.append(f"  - {when}  {name}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(summarize(gather()))
