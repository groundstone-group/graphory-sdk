# Worked example: walking the suggestion queue

A representative loop showing how the agent walks the queue, presents recommendations, and executes the user's response. Use this as the canonical reference for the skill's interaction pattern.

---

## Turn 1 - user triggers the skill

> **User**: clean up my suggestions

## Turn 2 - agent pulls a batch and recommends

(The agent calls `get_suggestions(status="pending", limit=20)` and inspects each entry.)

> **Agent**:
>
> Pulled 14 pending suggestions. My recommendations:
>
> ```
>  1. [CONFIRM]  merge "Sarah Chen <sarah@acme.com>" + "Sarah Chen <sarah.chen@acme.com>"
>                Same name, same domain, mailbox alias variation. High confidence.
>  2. [CONFIRM]  link Cloze contact "Marcus Lee" -> Gmail contact "marcus@helix.com"
>                Same name + you've emailed marcus@helix.com on threads
>                that match the Cloze deal log. Cross-source mirror, very common.
>  3. [REJECT]   merge "John Smith <john@acme.com>" + "John Smith <jsmith@helix.com>"
>                Different companies, no overlapping threads. Probably two
>                different Johns.
>  4. [SKIP]     merge "M. Park" + "Marcus Park"
>                Could be Marcus, could be Mei or Mike. Worth a human eyeball.
>  5. [CONFIRM]  unresolved relationship "Geolo Capital" -> existing org "Geolo Capital, LLC"
>                Same name, just legal-entity suffix. Standard normalization.
>  6. [REJECT]   unresolved relationship "Apollo" -> existing person "Apollo Park"
>                The mention is in a sentence about Apollo Global Management.
>                Different Apollo.
>  7. [SKIP]     merge "Sales Team" (in Slack) + "sales@acme.com" (Gmail)
>                One is a channel, one is an inbox alias. They're related
>                but I don't think we should treat them as the same entity.
>                Your call.
>  ...
>
> Tell me which to apply: "do all CONFIRMs", "do 1 2 5", "skip everything", etc.
> ```

## Turn 3 - user approves a subset

> **User**: do all confirms and rejects, leave the skips

## Turn 4 - agent executes and summarizes

(The agent loops through items 1, 2, 3, 5, 6 and calls `confirm_suggestion` or `reject_suggestion` per the recommendation. Items 4 and 7 are left untouched.)

> **Agent**:
>
> Done.
>
> ```
>   Confirmed: 3 (1 merge, 1 cross-source link, 1 unresolved-relationship link)
>   Rejected:  2
>   Skipped:   2 (left in the queue for you)
> ```
>
> The merged Sarah Chen now shows as one contact across both mailboxes. Marcus Lee in Cloze and the Gmail thread history are linked. The Geolo Capital mention is now hard-linked to the existing org.
>
> Want me to pull the next batch? Roughly 7 more suggestions are still in the queue.

---

## What NOT to do

**Never** call `confirm_suggestion` / `reject_suggestion` without an explicit approval message from the user in the prior turn. The whole point of the queue is human-in-the-loop. If the user says "go ahead" without naming items, ask them which ones - don't assume "all".

**Never** silently execute on the SKIPs because they "look fine on second thought". A SKIP is the agent's vote to leave it for the user; flipping it without asking violates the contract.

**Never** rubber-stamp the queue. If the agent finds itself recommending CONFIRM on 18 of 20 in a row with no real evidence, that's a sign to slow down and look harder, not to power through.
