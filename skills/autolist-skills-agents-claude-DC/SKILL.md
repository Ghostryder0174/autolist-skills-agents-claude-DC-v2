---
name: autolist-skills-agents-claude-DC
description: Startup layer run on every prompt by a UserPromptSubmit hook. Applies the startup skills in order, then routes the request to the best installed skills or agents from a cached header index, so the user never types a /command. Use when the hook line "autolist:" appears, when the user asks which skills or agents exist, or to classify newly installed skills.
---

# autolist-skills-agents-claude-DC

The hook `autolist.py` does the work, not this file. On every prompt it prints a few lines that start with `autolist:`. Read them and act on them. Do not open this file or the index for routine prompts.

## What the hook does

1. It reads only the frontmatter (`name`, `description`) of every skill, agent and plugin command: `~/.claude/skills`, `~/.claude/agents` and enabled plugins.
2. It caches the result in `~/.claude/cache/autolist/index.json`. It rebuilds the index only when the install changes: modification times of `installed_plugins.json`, `settings.json`, `classes.json`, and every personal `SKILL.md`.
3. It matches the prompt against names and descriptions. French words are mapped to English, and rare words weigh more. It prints at most 4 candidates.
4. It prints nothing for `/commands` or for prompts under 8 characters.

## What Claude does with the lines

1. **Startup**, in this order:
   1. `gestionnaire-de-skill-dc`: pick the model, the mode and the chain.
   2. `caveman`: the response mode, already injected by its own hook.
   3. `ponytail` and `karpathy-guidelines`: only for code.
2. **Candidates**: if the prompt is a task, invoke the most relevant candidate with the Skill tool, or the Agent tool for an agent. Do not wait for a `/command`. If no candidate fits, ignore them. For a chat message, invoke nothing.
3. **Demand skills**: never trigger these automatically. They ask questions or wait for input. The list is in `classes.json` under `demand`. Run one only if the user names it or plainly asks for it ("grille-moi", "interview", "configure ECC").
4. **New installs**: the hook classifies each new skill or agent on its own:
   - as `demande` if its description describes an interview, a wizard or a confirmation;
   - as `secondaire` otherwise.

   If a description looks like a startup rule (always-on, every prompt, response mode, model routing), the hook marks it "A TRANCHER". Ask the user one question: should it be startup or secondary? Then edit `classes.json`.

## Editing the classification

`classes.json` sits next to this file. Editing it triggers an index rebuild on the next prompt.

- `startup`: ordered list. A note in parentheses is a condition, for example `(si code)`.
- `demand`: short names never routed automatically.
- `pending`: entries waiting for the user's decision.
- `known`: everything already classified. Do not edit it by hand.

## Limits

- A hook cannot change the session model. `gestionnaire-de-skill-dc` recommends one, and `~/.claude/hooks/subagent-router.py` sets the model for subagents.
- Matching uses keywords, not an LLM. It costs zero tokens to compute and about 60 to 120 tokens of context per prompt.
