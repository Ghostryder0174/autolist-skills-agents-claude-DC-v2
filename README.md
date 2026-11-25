# autolist-skills-agents-claude-DC-v2

Une couche de démarrage pour Claude Code. À chaque prompt, elle rappelle l'ordre des skills de démarrage, puis propose les skills et agents installés qui correspondent à la demande. Tu n'as plus besoin de taper une `/commande` ni de connaître le nom d'un skill.

## Fonctionnement

Un hook `UserPromptSubmit` lance `autolist.py` à chaque prompt.

1. Le script lit uniquement l'en-tête (`name`, `description`) de chaque skill, agent et commande de plugin, jamais leur contenu complet.
2. Il garde le résultat en cache dans `~/.claude/cache/autolist/index.json`. Le cache n'est reconstruit que si les installations changent : plugins, `settings.json`, `classes.json` ou un `SKILL.md` personnel.
3. Il compare le prompt aux noms et descriptions. Les mots français sont traduits vers l'anglais et les mots rares comptent davantage. Il propose au plus 4 candidats.
4. Il ajoute quelques lignes de contexte, environ 120 tokens, en 0,2 s une fois le cache prêt :

```
autolist: demarrage = gestionnaire-de-skill-dc > caveman:caveman > ponytail:ponytail (si code) > ...
autolist: candidats = claude-seo:seo-audit (skill), claude-seo:seo (skill), ...
autolist: skills de demande = jamais auto, seulement si l'utilisateur les nomme.
```

Le script n'ajoute rien pour un prompt de moins de 8 caractères ou qui commence par `/`. S'il plante, il n'empêche jamais ton prompt de passer.

## Trois groupes

| Groupe | Effet |
|---|---|
| Démarrage | appliqué en premier, dans l'ordre défini par `startup` |
| Secondaire | proposé comme candidat, jamais chargé d'avance |
| Demande | skills qui posent des questions ou attendent une réponse (grilling, office-hours, wizards…) : jamais déclenchés automatiquement |

Quand tu installes un nouveau skill ou agent, il est classé tout seul :

- en **demande** si sa description parle d'interview, d'assistant de configuration ou de confirmation ;
- en **secondaire** sinon.

Si sa description ressemble à une règle de démarrage (always-on, chaque prompt, mode de réponse), il est marqué « A TRANCHER », et Claude te demande où le ranger.

La classification se trouve dans `skills/autolist-skills-agents-claude-DC/classes.json` et se modifie à la main.

## Installation (Windows)

Prérequis : Claude Code, Python 3 (lanceur `py`) et Node.js.

```powershell
git clone https://github.com/Ghostryder0174/autolist-skills-agents-claude-DC-v2
cd autolist-skills-agents-claude-DC-v2
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Option `-DisableSuperpowersHook` : empêche le plugin superpowers d'injecter `using-superpowers` au démarrage de chaque session, car il fait doublon avec ce routeur. Une mise à jour du plugin réactive cette injection.

Le script sauvegarde `settings.json` dans `~/.claude/backups/` avant de le modifier, et n'ajoute jamais le hook deux fois. Ouvre ensuite une nouvelle session Claude Code.

## Limites

- Les candidats sont choisis par mots-clés, sans appel à un LLM. C'est Claude qui retient le plus pertinent, ou aucun.
- Un hook ne peut pas changer le modèle de la session. Il ne peut que le recommander.
- L'ordre de démarrage par défaut (`gestionnaire-de-skill-dc`, `caveman`, `ponytail`, `karpathy-guidelines`) suppose que ces skills sont installés. Modifie `startup` dans `classes.json` selon ta configuration.

<!-- LISTE:START (généré, ne pas éditer à la main) -->
## Liste complète des skills et agents

Inventaire de la configuration de référence : **558 skills, 95 agents, 103 commandes**. Seuls les en-têtes sont listés. Sur ta machine, autolist reconstruit cette liste à partir de ce qui est réellement installé.

### Démarrage (appliqués en premier, dans cet ordre)

| # | Nom | Source | Description |
|---|---|---|---|
| 1 | `gestionnaire-de-skill-dc` | perso | Gestionnaire de skill DC, the skill manager. Turns a plain-French request into the right model, response mode and chain of installed skil… |
| 2 | `caveman` | caveman | Terse caveman voice: answer first, fluff gone, every technical fact kept. Use for /caveman, "caveman mode", "talk like caveman", "be brie… |
| 3 | `ponytail` | ponytail | Lazy senior dev mode: the smallest change that fully solves the task, and a reply a busy human understands in one read. Use on any coding… |
| 4 | `karpathy-guidelines` | andrej-karpathy-skills | Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, m… |

### Demande (jamais déclenchés automatiquement)

| Nom | Source | Type | Description |
|---|---|---|---|
| `caveman-learn` | caveman | skill | Act on a Caveman learn report - review the ranked token sinks, apply cost-lowering fixes with per-edit consent, and report what those fix… |
| `caveman-setup` | caveman | skill | Wire a repository through the Caveman Cloud gateway so every LLM request is measured, with no behavior change. Use for "set up caveman" o… |
| `brand-discovery` | ecc | skill | Run a structured, resumable multi-session brand identity interview across 8 modules (purpose, positioning, audience, personality, voice,… |
| `configure-ecc` | ecc | skill | Run the conversational ECC setup wizard inside the current harness: inventory the install, collect scope (user/project/local) and hook mo… |
| `hookify-configure` | ecc | command | Enable or disable hookify rules interactively |
| `operator-approval-loop` | ecc | skill | Operator approval contract with internal filing notices for agent-drafted outbound messages, hashed drafts, epoch-keyed decisions, durabl… |
| `orch-add-feature` | ecc | command | Orchestrate building a brand-new feature end to end — research, plan, TDD, review, gated commit. Wrapper that kicks off the orch-add-feat… |
| `orch-add-feature` | ecc | skill | Orchestrate building a brand-new feature end to end — research, plan, TDD implementation, review, and gated commit — by delegating each p… |
| `orch-build-mvp` | ecc | command | Orchestrate bootstrapping a working MVP from a design/spec doc — ingest, slice, scaffold, TDD, review, gated commit (reuses the GAN harne… |
| `orch-build-mvp` | ecc | skill | Orchestrate bootstrapping a working MVP from a design or spec document — ingest the SDD/PRD, plan thin vertical slices, scaffold the firs… |
| `orch-change-feature` | ecc | command | Orchestrate altering an existing, working feature to new desired behavior — update tests to the new spec, change impl, review, gated comm… |
| `orch-change-feature` | ecc | skill | Orchestrate altering an existing, working feature to new desired behavior — update its tests to the new spec, change the implementation t… |
| `orch-fix-defect` | ecc | command | Orchestrate fixing a bug — reproduce it as a failing regression test, fix to green, review, gated commit. Wrapper for the orch-fix-defect… |
| `orch-fix-defect` | ecc | skill | Orchestrate fixing a bug — reproduce it as a failing regression test, fix to green, review, and gated commit — by delegating each phase t… |
| `orch-pipeline` | ecc | skill | Shared orchestration engine behind the orch-* skill family — the gated Research-Plan-TDD-Review-Commit pipeline, size classifier, agent a… |
| `orch-refine-code` | ecc | command | Orchestrate a behavior-preserving refactor — confirm tests green, restructure without changing behavior, keep green, review, gated commit… |
| `orch-refine-code` | ecc | skill | Orchestrate a behavior-preserving refactor — confirm tests are green, restructure without changing behavior, keep tests green, review, an… |
| `plan` | ecc | command | Restate requirements, assess risks, and create step-by-step implementation plan. WAIT for user CONFIRM before touching any code. Use for… |
| `plan-canvas` | ecc | command | Open a plan or HTML artifact in the browser Plan Canvas for annotate-and-approve review. This is a thin slash-command entrypoint over the… |
| `plan-canvas` | ecc | skill | Open plans and HTML artifacts in a local browser canvas where the human annotates elements, chats, and approves or requests changes witho… |
| `plan-prd` | ecc | command | Generate a lean, problem-first PRD and hand off to /plan for implementation planning. |
| `prp-prd` | ecc | command | Interactive PRD generator - problem-first, hypothesis-driven product spec with back-and-forth questioning |
| `tasteforge-video` | ecc | skill | Use for file-driven multimodal image, video, and 3D-asset discovery; taste interviews; distill or apply workflows; style-pack validation;… |
| `team-builder` | ecc | skill | Interactive picker that discovers available agent personas via the claude agents command and agents/ markdown globs, groups them into dom… |
| `token-budget-advisor` | ecc | skill | Offer a choice of response depth (25%/50%/75%/100%) with token estimates before answering, then answer at that level. Use when the user a… |
| `ui-canvas` | ecc | command | Preview a UI component mockup in the browser UI Canvas where the user hand-edits it (move, resize, text, delete, restyle), tests it acros… |
| `ui-canvas` | ecc | skill | Preview a UI component mockup in a local browser canvas where the human directly edits it (move, resize, edit text, delete, restyle), swi… |
| `i-have-adhd` | i-have-adhd | skill | Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state across turns, suppress tangents, gi… |
| `grill-me` | mattpocock-skills | skill | A relentless interview to sharpen a plan or design. |
| `grill-with-docs` | mattpocock-skills | skill | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| `grilling` | mattpocock-skills | skill | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' t… |
| `improve-codebase-architecture` | mattpocock-skills | skill | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| `loop-me` | mattpocock-skills | skill | Grill me about specs for the workflows I want to build, within this workspace. |
| `setup-matt-pocock-skills` | mattpocock-skills | skill | Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before… |
| `setup-pre-commit` | mattpocock-skills | skill | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-c… |
| `setup-ts-deep-modules` | mattpocock-skills | skill | Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reachable o… |
| `to-questionnaire` | mattpocock-skills | skill | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. |
| `triage` | mattpocock-skills | skill | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs. |
| `wizard` | mattpocock-skills | skill | Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting… |
| `gstack-autoplan` | perso | skill | Auto-review pipeline — runs the CEO, design, eng and DX reviews in order (lean run: one reviewer), auto-deciding. Use for: run all review… |
| `gstack-design-consultation` | perso | skill | Design consultation: understands your product, researches the landscape, proposes a complete design system (aesthetic, typography, color,… |
| `gstack-design-shotgun` | perso | skill | Design shotgun: generate multiple AI design variants, open a comparison board, collect structured feedback, and iterate. Use for: explore… |
| `gstack-office-hours` | perso | skill | YC Office Hours — two modes. Use for: brainstorm this, is this worth building. (gstack) |
| `gstack-plan-ceo-review` | perso | skill | CEO/founder-mode plan review. Use for: think bigger, expand scope, strategy review. (gstack) |
| `gstack-plan-design-review` | perso | skill | Designer's eye plan review — interactive, like CEO and Eng review. Use for: design plan review, review ux plan. (gstack) |
| `gstack-plan-devex-review` | perso | skill | Interactive developer experience plan review. Use for: developer experience review, dx plan review. (gstack) |
| `gstack-plan-eng-review` | perso | skill | Use when you plan a feature before building it, or review a plan: locks in architecture, data flow, diagrams, edge cases, test coverage a… |
| `gstack-plan-tune` | perso | skill | Self-tuning question sensitivity + developer psychographic for gstack (v1: observational). Use for: tune questions, stop asking me that.… |
| `gstack-setup-browser-cookies` | perso | skill | Import cookies from your real Chromium browser into the headless browse session. Use for: import browser cookies, login to test site. (gs… |
| `gstack-setup-deploy` | perso | skill | Configure deployment settings for /land-and-deploy. Use for: configure deploy, setup deployment. |
| `gstack-setup-gbrain` | perso | skill | Set up gbrain for this coding agent: install the CLI, initialize a local PGLite or Supabase brain, register MCP, capture per-remote trust… |
| `brainstorming` | superpowers | skill | You MUST use this before any creative work - creating features, building components, adding functionality, modifying behavior, or plannin… |
| `finishing-a-development-branch` | superpowers | skill | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work |
| `using-superpowers` | superpowers | skill | Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including cla… |

### Secondaires (proposés selon la demande)

<details><summary>Skills — perso (`~/.claude/skills`) (89)</summary>

| Nom | Description |
|---|---|
| `_gstack-command` | Picks the gstack skill that fits a request: planning, review, QA, shipping, docs, security or design. Use for: gstack, which gstack skill… |
| `agent-desktop` | Operate desktop applications on macOS, Windows and Linux through native accessibility trees, using the agent-desktop CLI. Use when an AI… |
| `agent-desktop-windows` | Windows platform guide for the agent-desktop CLI. Lists per command group what works on Windows and what refuses, the first-contact gotch… |
| `agent-reach` | 只读读取各平台内容：搜索、读帖、看评论、取字幕、查行情和职位。 Use when 用户提到或贴出链接：小红书/xiaohongshu、B站/bilibili、Twitter/X、Reddit、 YouTube（字幕、转录）、GitHub、V2EX、雪球/股票行情、Linke… |
| `animate` | Build an animation from scratch, making the decisions in the order that determines whether it feels right — should it animate at all, wha… |
| `animate-expo` | Build animations in React Native and Expo, making the decisions in the order that determines whether they feel right — should it animate,… |
| `animation-performance` | Keep web animations inside the frame budget — animate composite-only properties, keep motion off the main thread when the page is busy, a… |
| `animation-vocabulary` | Reverse-lookup glossary that turns a vague description of a web animation or motion effect into its exact term ("the bouncy thing when a… |
| `apple-design` | Apple's approach to interface design and fluid, physical motion, translated for the web. Use when building or reviewing gesture-driven UI… |
| `ask-emil` | Ask which skill or flow fits your situation. A router over the skills in this repo. |
| `ask-sonner` | Guide to Sonner, the React toast library — install and wire up the Toaster, pick the right toast() call, promise and loading toasts, upda… |
| `autolist-skills-agents-claude-DC` | Startup layer run on every prompt by a UserPromptSubmit hook. Applies the startup skills in order, then routes the request to the best in… |
| `break-ui` | Try to break a piece of UI by feeding it worst-case data — long names, unbreakable emails, one-letter names, missing fields, huge counts,… |
| `choreograph` | Coordinate several elements that animate together — decide what moves, in what order, how much they overlap, and what stays still — so a… |
| `cso-linux` | Run gstack's security audit (/gstack-cso) inside the WSL Ubuntu VM so comprehensive mode works (Docker-isolated reproduction, scanners gi… |
| `deploy-to-vercel` | Deploy applications and websites to Vercel. Use when the user requests deployment actions like "deploy my app", "deploy and give me the l… |
| `emil-design-eng` | Emil Kowalski's design-engineering philosophy for UI polish, component design, animation decisions, and the invisible details that make s… |
| `find-animation-opportunities` | Search a codebase or UI for places that don't animate but should, and reject everything that shouldn't. Read-only; it proposes motion wit… |
| `gestures` | Build drag, swipe, and sheet interactions that track the finger 1:1 and stay interruptible. Use when building or fixing anything the user… |
| `graphify` | Use for any question about a codebase, its architecture, file relationships, or project content — especially when graphify-out/ exists, w… |
| `gstack` | Picks the gstack skill that fits a request: planning, review, QA, shipping, docs, security or design. Use for: gstack, which gstack skill… |
| `gstack-benchmark` | Web performance regression detection. Use for: web performance benchmark, check page speed. (gstack) |
| `gstack-benchmark-models` | Cross-model benchmark for gstack skills. Use for: cross model benchmark, compare claude gpt gemini. (gstack) |
| `gstack-browse` | Drive a real browser through Aside: open a page, read it, click through a flow, take screenshots, check console errors. Use for: browse a… |
| `gstack-build-check` | Use when coding: run the checks and tests /ship picks until green. Use for: run the checks, make the tests pass, make it green. (gstack) |
| `gstack-canary` | Post-deploy canary monitoring. Use for: monitor after deploy, canary check. (gstack) |
| `gstack-careful` | Safety guardrails for destructive commands. Use for: be careful, warn before destructive, safety mode. (gstack) |
| `gstack-codex` | OpenAI Codex CLI wrapper — three modes. Use for: codex review, second opinion, outside voice challenge. (gstack) |
| `gstack-connect-chrome` | Launch GStack Browser — AI-controlled Chromium with the sidebar extension baked in. Use for: open gstack browser, launch chromium. |
| `gstack-context-restore` | Restore working context saved earlier by /context-save. Use for: resume where i left off, restore context, where was i. (gstack) |
| `gstack-context-save` | Save working context. Use for: save progress, save state, save my work, context save. (gstack) |
| `gstack-cso` | Security audit: supported static findings; qualified profiles add reproduction and repair candidates. Use for: security audit, check for… |
| `gstack-design-html` | Design finalization: generates production-quality Pretext-native HTML/CSS. Use for: build the design, code the mockup, make design real.… |
| `gstack-design-motion` | Design motion: animate an approved design into a seamless MP4 and GIF loop. Use for: animate this design, make a showcase loop. (gstack) |
| `gstack-design-review` | Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then fixes t… |
| `gstack-deslop-shared-libs` | Find worthwhile shared-code extractions in recent work. Use for: find code worth sharing. (gstack) |
| `gstack-devex-review` | Live developer experience audit. Use for: live dx audit, test developer experience. (gstack) |
| `gstack-diagram` | Turn an English description (or mermaid source) into a diagram triplet: the source, an editable .excalidraw file you can open on excalidr… |
| `gstack-document-generate` | Generate missing documentation from scratch for a feature, module, or entire project. Use for: write docs for this, generate documentatio… |
| `gstack-document-release` | Release documentation audit. Use for: update docs after ship, document what changed. (gstack) |
| `gstack-eval-plan` | Preregister a paid eval (bars, arms, decoys, stop rules), dry-run it at zero cost, then run a three-item priced pilot whose spend table g… |
| `gstack-freeze` | Restrict file edits to a specific directory for the session. Use for: freeze edits to directory, lock editing scope. (gstack) |
| `gstack-guard` | Full safety mode: destructive command warnings + directory-scoped edits. Use for: full safety mode, guard against mistakes. (gstack) |
| `gstack-health` | Code quality dashboard. Use for: code health check, quality dashboard. (gstack) |
| `gstack-ios-clean` | Remove the DebugBridge SPM package and all #if DEBUG wiring from an iOS app. Use for: clean the ios debug bridge, remove debugbridge. (gs… |
| `gstack-ios-design-review` | Visual design audit for iOS apps on real hardware. Use for: review the ios design, audit the iphone app visuals. (gstack) |
| `gstack-ios-fix` | Autonomous iOS bug fixer. Use for: fix this ios bug, patch the iphone app. (gstack) |
| `gstack-ios-qa` | Live-device iOS QA for SwiftUI apps. Use for: ios qa, test the iphone app, test the ipad app. (gstack) |
| `gstack-ios-sync` | Regenerate the iOS debug bridge against the latest upstream gstack templates. Use for: resync the ios debug bridge, regenerate ios access… |
| `gstack-land-and-deploy` | Land and deploy workflow. Use for: merge and deploy, land the pr, ship to production. (gstack) |
| `gstack-landing-report` | Read-only queue dashboard for workspace-aware ship. Use for: landing report, version queue, ship queue. (gstack) |
| `gstack-learn` | Manage project learnings. Use for: show learnings, what have we learned. |
| `gstack-make-pdf` | Turn any markdown file into a publication-quality PDF. Use for: markdown to pdf, generate pdf, make pdf, export pdf. (gstack) |
| `gstack-modernize` | Bring an aging PR onto its current base and decide: MODERNIZE, REWORK or CLOSE. Use for: modernize this pr, rebase this old pr. (gstack) |
| `gstack-open-gstack-browser` | Launch GStack Browser — AI-controlled Chromium with the sidebar extension baked in. Use for: open gstack browser, launch chromium. |
| `gstack-pair-agent` | Pair a remote AI agent with your browser. Use for: pair with agent, connect remote agent. (gstack) |
| `gstack-qa` | Use when you test the site, API or CLI and fix bugs. Use for: qa test this, find bugs on site, test the site. (gstack) |
| `gstack-qa-only` | Report browser/API/CLI/job/worker/webhook bugs. Use for: qa report only, just report bugs, test but dont fix. (gstack) |
| `gstack-retro` | Weekly engineering retrospective. Use for: weekly retro, what did we ship. (gstack) |
| `gstack-review` | Use when you review a diff before it lands: local changes, a branch or a PR. Use for: review my changes, look over my diff, review this p… |
| `gstack-runaway-stopper` | Find runaway Capy threads and subagents, stop or rotate them safely, and prevent repeats. Use for: find runaway threads, stop runaway job… |
| `gstack-scrape` | Pull data from a web page through the Aside browser — your real, already signed-in sessions. Use for: scrape this page, get data from, pu… |
| `gstack-ship` | Ship it: merge the base, run tests, review the diff, bump VERSION and CHANGELOG, push and create a PR. Use for: ship it, create a pr, pus… |
| `gstack-skillify` | Codify the most recent successful /scrape flow into a permanent browser-skill on disk. Use for: skillify, codify this scrape, save this s… |
| `gstack-spec` | Turn vague intent into a precise, executable spec in five phases. Use for: spec this out, file an issue, write up a ticket. (gstack) |
| `gstack-sync-gbrain` | Keep gbrain current with this repo's code and refresh agent search guidance in CLAUDE.md. Use for: sync gbrain, refresh gbrain, reindex r… |
| `gstack-test-audit` | Find low-value or duplicate tests and the test-only code they keep alive. Use for: audit the test suite, find low-value tests. (gstack) |
| `gstack-ubicloud` | Run a heavy suite, build or eval on an ephemeral 16-vCPU Ubicloud VM: TTL-named VMs, a reaper, quota preflight and a hang watchdog. Use f… |
| `gstack-unfreeze` | Clear the freeze boundary set by /freeze, allowing edits to all directories again. Use for: unfreeze edits, unlock all directories. (gstack) |
| `gstack-upgrade` | Upgrade gstack to the latest version. Use for: upgrade gstack, update gstack version. |
| `gstack-write-skill` | Write a new agent skill or improve one without bloat: the edit ladder, levels, drift and size checks, full diets. Use for: write a skill,… |
| `improve-animations` | Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained implementat… |
| `learn-taste` | Turn a session's design corrections into rules, with their why, in DESIGN.md, a project skill, or a lint check. |
| `mobile-native` | Make a web app feel native on a phone — the small CSS and meta-tag fixes that separate "a website in a browser" from something that feels… |
| `obscura` | Operate and validate Obscura for JavaScript page loading, stealth browsing, anti-fingerprinting, tracker blocking, screenshots and visual… |
| `pick-ui-library` | Pick the library for a frontend task from a curated list — primitives, toasts, drawers, command menus, OTP, numbers, charts, virtualizati… |
| `playwright-cli` | Automate browser interactions, test web pages and work with Playwright tests. |
| `prototype` | Build multiple genuinely different versions of a UI piece you describe, rendered behind a visual picker so you can flip through them live… |
| `remove-animations` | Find the animations an interface doesn't need and remove them — motion on keyboard actions, high-frequency surfaces, functional data, and… |
| `review-animations` | Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. Default to flaggin… |
| `vercel-cli-with-tokens` | Deploy and manage projects on Vercel using token-based authentication. Use when working with Vercel CLI using access tokens rather than i… |
| `vercel-composition-patterns` | React composition patterns that scale. Use when refactoring components with boolean prop proliferation, building flexible component libra… |
| `vercel-optimize` | Use for Vercel cost and performance optimization on deployed projects, especially Next.js, SvelteKit, Nuxt, and limited Astro apps. Colle… |
| `vercel-react-best-practices` | React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refa… |
| `vercel-react-native-skills` | React Native and Expo best practices for building performant mobile apps. Use when building React Native components, optimizing list perf… |
| `vercel-react-view-transitions` | Guide for implementing smooth, native-feeling animations using React's View Transition API (`<ViewTransition>` component, `addTransitionT… |
| `web-design-guidelines` | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review… |
| `write-swift` | How to write modern Swift well — modeling with value types, Swift 6 data-race safety and approachable concurrency (@concurrent, main-acto… |
| `writing-guidelines` | Review docs/prose for Writing Guidelines compliance. Use when asked to "review my docs", "check writing style", "audit prose", "review do… |

</details>

<details><summary>Skills — plugin `caveman` (19)</summary>

| Nom | Description |
|---|---|
| `cavecrew` | When to delegate to `cavecrew-investigator` (locate code), `cavecrew-builder` (1-2 file edit) or `cavecrew-reviewer` (diff review) instea… |
| `caveman-commit` | Write a Conventional Commits message compressed to intent only. Use for "write a commit", "commit message", /commit or /caveman-commit. |
| `caveman-compress` | Compress a memory file such as CLAUDE.md or a todo list into caveman format to save input tokens, keeping a readable backup. Sends the fi… |
| `caveman-discover` | Find and label every LLM workflow in the repository so Caveman Cloud groups spend by workflow instead of one bucket. Use for "discover wo… |
| `caveman-evidence-review` | Read-only review of Caveman Cloud evidence: cost, Cave Score, workflows, traces, latency, errors, routing, savings. Use when asked what C… |
| `caveman-explore` | Read-only repository explorer for cold-start orientation, broad cross-file localization, or when a direct search failed. Skip it when the… |
| `caveman-help` | Quick-reference card for the three caveman skills and their commands. Trigger: /caveman-help or "caveman help". |
| `caveman-manage` | Inspect Caveman Cloud's experiment lifecycle and block unsafe execution. Use when asked to start, approve, cancel, promote or roll back a… |
| `caveman-optimize` | Turn a Caveman optimization observation into an operator-chosen candidate with a paired baseline evaluation. Use when asked to inspect or… |
| `caveman-review` | Compressed code review - one line per finding with location, problem and fix. Use for /caveman-review, "review this PR", or "review the d… |
| `caveman-stats` | Show recorded output and cache-read token usage and mode attribution for the current Claude Code session, or locate the host's native usa… |
| `investigate-first` | Diagnose ambiguous failures before editing. Use for unknown causes, intermittent behavior, performance regressions, or investigations nee… |
| `lean-build` | Build feature work with high overbuilding risk. Use for new behavior, product slices, or integrations where repository reuse, strict scop… |
| `megacave` | Caveman in Classical Chinese: 文言文 register, far fewer characters, technical terms verbatim. Invoke only with /megacave or /caveman wenyan… |
| `migration` | Implement reversible compatibility-safe transitions. Use for schema, data, API, protocol, configuration, or dependency migrations requiri… |
| `safe-refactor` | Restructure code while preserving behavior. Use for extraction, consolidation, ownership moves, or cleanup where verification must bracke… |
| `surgical-patch` | Fix bugs and small behavior changes at the narrowest responsible layer. Use when regression proof, preserved surrounding behavior, and ta… |
| `ultracave` | Caveman at maximum compression: fragments, one word when one word is enough, each fact once. Invoke only with /ultracave or /caveman ultr… |
| `verify-and-stop` | Prove existing work meets acceptance conditions without expanding scope. Use for validation-only tasks, completion checks, focused gate r… |

</details>

<details><summary>Agents — plugin `caveman` (3)</summary>

| Nom | Description |
|---|---|
| `cavecrew-builder` | Surgical 1-2 file edit. Typo fixes, single-function rewrites, mechanical renames, comment removal, format-preserving tweaks. Hard refuses… |
| `cavecrew-investigator` | Read-only code locator. Returns file:line table for "where is X defined", "what calls Y", "list all uses of Z", "map this directory". Out… |
| `cavecrew-reviewer` | Diff/branch/file reviewer. One line per finding, severity-tagged, no praise, no scope creep. Output format `path:line: <emoji> <severity>… |

</details>

<details><summary>Commandes — plugin `caveman` (1)</summary>

| Nom | Description |
|---|---|
| `caveman-init` | Drop the always-on caveman activation rule into the current repo for every IDE agent |

</details>

<details><summary>Skills — plugin `claude-seo` (29)</summary>

| Nom | Description |
|---|---|
| `seo` | Comprehensive SEO analysis for any website or business type. Full site audits, single-page analysis, technical SEO (crawlability, indexab… |
| `seo-agentic` | Audit and fix agent readiness: the Lighthouse Agentic Browsing fraction, accessibility tree for agents, robots.txt and Content-Signal for… |
| `seo-audit` | Run a full-site SEO audit and return a scored, prioritized report. Use only for site-wide checks; use seo-page for one URL or seo-technic… |
| `seo-backlinks` | Analyze a site's backlink profile, anchors, toxic signals, competitors, gaps, and disavow candidates. Use only when links or referring do… |
| `seo-bing` | Bing Webmaster Tools + IndexNow extension. Microsoft Copilot citations are fed by the Bing index; this skill makes Bing visibility, link… |
| `seo-cluster` | Cluster keywords by SERP overlap and design hub-and-spoke content architecture with internal links. Use for planning; `/seo cluster execu… |
| `seo-competitor-pages` | Generate SEO-optimized competitor comparison and alternatives pages. Covers "X vs Y" layouts, "alternatives to X" pages, feature matrices… |
| `seo-content` | Evaluate page content for usefulness, E-E-A-T, readability, thinness, and AI citation readiness, plus last-mile draft cleanup (AI-typical… |
| `seo-content-brief` | Generate competitive SEO content briefs with per-section word counts, competitor scoring, keyword placement guidance, and page-type templ… |
| `seo-dataforseo` | Live SEO data via DataForSEO MCP server: SERP analysis, keyword research (volume, difficulty, intent, trends), backlink profiles, on-page… |
| `seo-drift` | SEO drift monitoring: capture baselines of SEO-critical elements, detect changes, and track regressions over time. Git for SEO: baseline,… |
| `seo-ecommerce` | Analyze ecommerce SEO across product pages, product schema, Shopping visibility, marketplace signals, and keyword gaps. Use only for stor… |
| `seo-flow` | FLOW framework integration: evidence-led SEO using the Find → Leverage → Optimize → Win loop. Surfaces stage-specific AI prompts from the… |
| `seo-geo` | Audit and improve content for AI Overviews and answer engines, including citability, entity clarity, crawler access, brand signals, and p… |
| `seo-google` | Google SEO APIs: Search Console (Search Analytics, URL Inspection, Sitemaps), PageSpeed Insights v5, CrUX field data with 25-week history… |
| `seo-hreflang` | Hreflang and international SEO audit, validation, and generation. Detects common mistakes, validates language/region codes, and generates… |
| `seo-image-gen` | AI image generation for SEO assets: OG/social preview images, blog hero images, schema images, product photography, infographics. Powered… |
| `seo-images` | Image optimization analysis for SEO and performance. Checks alt text, file sizes, formats, responsive images, lazy loading, CLS preventio… |
| `seo-local` | Audit local SEO, including Google Business Profile, NAP consistency, citations, reviews, local schema, location pages, and multi-location… |
| `seo-maps` | Maps intelligence for local SEO: geo-grid rank tracking, GBP profile auditing via API, review intelligence across Google/Tripadvisor/Trus… |
| `seo-page` | Analyze one supplied URL across on-page, content, technical metadata, schema, images, and performance. Use only for a single-page review. |
| `seo-plan` | Strategic SEO planning for new or existing websites. Industry-specific templates, competitive analysis, content strategy, and implementat… |
| `seo-posthog` | PostHog MCP extension. PostHog analytics as a GA4 alternative or complement. Organic traffic, landing pages, device / country breakdowns,… |
| `seo-programmatic` | Programmatic SEO planning and analysis for pages generated at scale from data sources. Covers template engines, URL patterns, internal li… |
| `seo-schema` | Detect, validate, or generate Schema.org JSON-LD for a supplied page or entity. Use only when structured data or rich-result markup is re… |
| `seo-shopify` | Uncapped, sitemap-complete crawl of a Shopify storefront using the merchant's Crawler Access signature from a project-local .shopify-env,… |
| `seo-sitemap` | Analyze existing XML sitemaps or generate new ones with industry templates. Validates format, URLs, and structure. Use when user says "si… |
| `seo-sxo` | Diagnose search-experience and intent mismatches using SERP page types, user stories, and persona scoring. Use when ranking problems appe… |
| `seo-technical` | Audit technical SEO across crawlability, indexability, security, URLs, mobile, Core Web Vitals, rendering, structured data, and IndexNow.… |

</details>

<details><summary>Agents — plugin `claude-seo` (20)</summary>

| Nom | Description |
|---|---|
| `seo-agentic` | Agent-readiness analyst. Explains the Lighthouse Agentic Browsing fraction and audits the accessibility tree for agents, robots.txt and C… |
| `seo-backlinks` | Backlink profile analyst using free and paid sources. Fetches data from Moz API, Bing Webmaster Tools, Common Crawl web graphs, and verif… |
| `seo-cluster` | Semantic topic clustering analysis using SERP overlap methodology. Expands seed keywords, performs pairwise SERP comparison, classifies i… |
| `seo-content` | Content quality reviewer. Evaluates E-E-A-T signals, readability, content depth, AI citation readiness, and thin content detection. |
| `seo-dataforseo` | DataForSEO data analyst. Fetches live SERP data, keyword metrics, backlink profiles, on-page analysis, content analysis, business listing… |
| `seo-drift` | SEO drift analysis agent. Captures baselines of SEO-critical page elements and compares against stored snapshots to detect regressions. R… |
| `seo-ecommerce` | E-commerce SEO analyst. Validates product schema, analyzes Google Shopping and Amazon marketplace visibility, identifies pricing gaps, an… |
| `seo-flow` | FLOW framework prompt analyst. Reads the target URL, selects relevant FLOW stage prompts, applies them, and returns structured output wit… |
| `seo-geo` | GEO and AI search specialist. Analyzes AI crawler accessibility, llms.txt presence (optional; ignored by Google Search), passage-level ci… |
| `seo-google` | Google SEO API analyst. Fetches CWV field data via CrUX, indexation status via GSC, and organic traffic via GA4 for enriched audit data. |
| `seo-image-gen` | SEO image analyst. Audits existing OG/social preview images, identifies missing or low-quality images, and creates an image generation pl… |
| `seo-local` | Local SEO specialist. Analyzes GBP signals, NAP consistency, citations, reviews, local schema, location page quality, and industry-specif… |
| `seo-maps` | Maps intelligence specialist. Geo-grid rank tracking, GBP profile auditing, review intelligence, cross-platform NAP verification, and com… |
| `seo-performance` | Performance analyzer. Measures and evaluates Core Web Vitals and page load performance. |
| `seo-posthog` | PostHog analytics analyst. Uses the PostHog MCP server to fetch organic search traffic, top landing pages, device / country breakdowns, a… |
| `seo-schema` | Schema markup expert. Detects, validates, and generates Schema.org structured data in JSON-LD format. |
| `seo-sitemap` | Sitemap architect. Validates XML sitemaps, generates new ones with industry templates, and enforces quality gates for location pages. |
| `seo-sxo` | Search Experience Optimization analyst. Performs SERP backwards analysis to detect page-type mismatches, derives user stories from intent… |
| `seo-technical` | Technical SEO specialist. Analyzes crawlability, indexability, security, URL structure, mobile optimization, Core Web Vitals, and JavaScr… |
| `seo-visual` | Visual analyzer. Captures screenshots, tests mobile rendering, and analyzes above-the-fold content using Playwright. |

</details>

<details><summary>Skills — plugin `ecc` (314)</summary>

| Nom | Description |
|---|---|
| `accessibility` | Design, implement, and audit accessible UI to WCAG 2.2 Level AA across Web, iOS, and Android — semantic ARIA roles and labels, accessibil… |
| `agent-architecture-audit` | Full-stack diagnostic for agent and LLM applications. Audits the 12-layer agent stack for wrapper regression, memory pollution, tool disc… |
| `agent-eval` | Head-to-head comparison of coding agents (Claude Code, Aider, Codex, etc.) on custom tasks with pass rate, cost, time, and consistency me… |
| `agent-harness-construction` | Design and optimize AI agent action spaces, tool definitions, and observation formatting for higher completion rates. Use when defining o… |
| `agent-introspection-debugging` | Structured self-debugging workflow for AI agent failures using capture, diagnosis, contained recovery, and introspection reports. Use whe… |
| `agent-payment-x402` | Add x402 payment execution to AI agents with per-task budgets, spending controls, and non-custodial wallets. Supports Base through agentw… |
| `agent-runtime-gateway-smoke-test` | Verify a local agent API, temporary gateway tunnel, and remote sandbox callback with a tool-free task, then restore the original app conn… |
| `agent-security-hardening` | Security hardening guidance for AI agent frameworks that process untrusted content, invoke tools, write workspace files, manage runtime i… |
| `agent-self-evaluation` | Use after completing any non-trivial task. The agent self-rates its output on 5 axes — accuracy, completeness, clarity, actionability, co… |
| `agent-sort` | Build an evidence-backed ECC install plan for a specific repo by sorting skills, commands, rules, hooks, and extras into DAILY vs LIBRARY… |
| `agentic-engineering` | Operate as an agentic engineer using eval-first execution, decomposition, and cost-aware model routing. Use when planning or executing en… |
| `agentic-os` | Build persistent multi-agent operating systems on Claude Code. Covers kernel architecture, specialist agents, slash commands, file-based… |
| `ai-first-engineering` | Engineering operating model for teams where AI agents generate a large share of implementation output. Use when setting team process, rev… |
| `ai-regression-testing` | Regression testing strategies for AI-assisted development. Sandbox-mode API testing without database dependencies, automated bug-check wo… |
| `android-clean-architecture` | Clean Architecture patterns for Android and Kotlin Multiplatform projects — module structure, dependency rules, UseCases, Repositories, a… |
| `angular-developer` | Generates Angular code and provides architectural guidance. Trigger when creating projects, components, or services, or for best practice… |
| `api-connector-builder` | Build a new API connector or provider by matching the target repo's existing integration pattern exactly. Use when adding one more integr… |
| `api-design` | REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting f… |
| `architecture-decision-records` | Capture architectural decisions as numbered ADR markdown files in docs/adr/ with context, alternatives considered, consequences, and an i… |
| `article-writing` | Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form content in a distinctive voice derived from supplie… |
| `automation-audit-ops` | Evidence-first automation inventory and overlap audit workflow for ECC. Use when the user wants to know which jobs, hooks, connectors, MC… |
| `autonomous-agent-harness` | Transform Claude Code into a fully autonomous agent system with persistent memory, scheduled operations, computer use, and task queuing.… |
| `autonomous-loops` | Patterns and architectures for autonomous Claude Code loops — from simple sequential pipelines to RFC-driven multi-agent DAG systems. Ret… |
| `backend-patterns` | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API ro… |
| `benchmark` | Measure performance baselines and detect regressions across browser Core Web Vitals (LCP, INP, CLS, page weight), API endpoint latency pe… |
| `benchmark-methodology` | Score a scoped competitor set into comparable profile cards: nine weighted dimensions (positioning, voice, visual craft, offer packaging,… |
| `benchmark-optimization-loop` | - Turn a user's improvement goal into a bounded benchmark-guided loop: define success and hard constraints, establish a baseline, test on… |
| `bengali-nlp` | Bengali (Bangla) text processing patterns including Unicode normalization, script detection, tokenization, conjunct handling, and Bangla-… |
| `blender-motion-state-inspection` | Inspects Blender characters, rigs, poses, animation retargeting, ground contact, facing direction, or model-vs-motion alignment where scr… |
| `blueprint` | Turn a one-line objective into a step-by-step construction plan for multi-session, multi-agent engineering projects: one-PR-sized steps w… |
| `brand-voice` | Build a source-derived writing style profile from real posts, essays, launch notes, docs, or site copy, then reuse that profile across co… |
| `brownfield-retrospective` | Run the ECC engineering process retroactively against an existing project slice. Audit current state, reconstruct past decisions, produce… |
| `browser-qa` | Run automated post-deploy UI verification with a browser automation MCP (claude-in-chrome, Playwright, or Puppeteer): console-error and C… |
| `bun-runtime` | Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support. |
| `canary-watch` | Monitors and verifies deployed URLs after releases by checking HTTP endpoints, SSE streams, static assets, console errors, and performanc… |
| `carrier-relationship-management` | Manage truckload, LTL, and intermodal carrier portfolios: sourcing and FMCSA vetting, freight rate and fuel-surcharge negotiation, RFPs a… |
| `change-impact` | - Perform evidence-backed impact analysis before changing code, data, interfaces, or governance documents, then compare the planned impac… |
| `cisco-ios-patterns` | Cisco IOS and IOS-XE review patterns for show commands, config hierarchy, wildcard masks, ACL placement, interface hygiene, and safe chan… |
| `ck` | Persistent per-project memory for Claude Code (Context Keeper) driven by deterministic Node.js /ck commands: init, save, resume, info, li… |
| `click-path-audit` | Trace every user-facing button/touchpoint through its full state change sequence to find bugs where functions individually work but cance… |
| `clickhouse-io` | ClickHouse database patterns, query optimization, analytics, and data engineering best practices for high-performance analytical workload… |
| `code-tour` | Create CodeTour `.tour` files — persona-targeted, step-by-step walkthroughs with real file and line anchors. Use for onboarding tours, ar… |
| `codebase-onboarding` | Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a sta… |
| `codehealth-mcp` | Real-time structural Code Health via CodeScene MCP — review before edits, verify score deltas after changes, gate commits and PRs. Use wh… |
| `coding-standards` | Baseline cross-project coding conventions for naming, readability, immutability, and code-quality review. Use detailed frontend or backen… |
| `competitive-platform-analysis` | Use when scoping a competitive landscape — identifying, categorising, and score-filtering a competitor set before any benchmarking begins… |
| `competitive-report-structure` | Assemble scored competitor profile cards (from benchmark-methodology) into a decision-grade competitive report with landscape map, compet… |
| `compose-multiplatform-patterns` | Compose Multiplatform and Jetpack Compose patterns for KMP projects — state management, navigation, theming, performance, and platform-sp… |
| `config-gc` | Garbage collection for your Claude Code configuration. Periodically scans ~/.claude (skills, memory, hooks, permissions, MCP servers, cac… |
| `config-health` | Runtime configuration integrity monitoring for Claude Code. Detects config drift, rule staleness, and hook wiring gaps at startup, with a… |
| `connections-optimizer` | Reorganize the user's X and LinkedIn network with review-first pruning, add/follow recommendations, and channel-specific warm outreach dr… |
| `content-engine` | Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters, and repurposed multi-platform campaigns. Use when t… |
| `content-hash-cache-pattern` | Cache expensive file processing results using SHA-256 content hashes — path-independent, auto-invalidating, with service layer separation… |
| `context-and-decisions` | - Govern stable domain context with a narrowly scoped CONTEXT.md when needed, and route hard-to-reverse decisions to ECC's existing archi… |
| `context-budget` | Routes live context checks to the native Codex or Claude Code meter without scanning files, and performs a bounded static component audit… |
| `continuous-agent-loop` | Patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls. Use when running an agent loop that must… |
| `continuous-learning` | [DEPRECATED - use continuous-learning-v2] Legacy v1 stop-hook skill extractor. v2 is a strict superset with instinct-based, project-scope… |
| `continuous-learning-v2` | Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring, and evolves them into… |
| `contract-first` | Coordinate frontend/backend or service-to-service work through one authoritative machine-checkable contract (OpenAPI, AsyncAPI, Protocol… |
| `conventional-commit-review` | Reviews staged changes and drafts a Conventional Commits-compliant commit message with the right type, scope, and length. Use before comm… |
| `cost-aware-llm-pipeline` | Cost optimization patterns for LLM API usage — model routing by task complexity, budget tracking, retry logic, and prompt caching. Use wh… |
| `cost-tracking` | Track and report Claude Code token usage, spending, and budgets from the local ECC cost-tracker metrics log. Use when the user asks about… |
| `council` | Convene a four-voice council for ambiguous decisions, tradeoffs, and go/no-go calls. Use when multiple valid paths exist and you need str… |
| `council-multi-model` | Add one optional external Codex critique after the existing council has produced a decision draft. Use when an ambiguous, high-consequenc… |
| `counterparty-channel-discipline` | Per-channel strict prompts, mention gating, silent observation, and a communication autonomy policy for agents that sit in shared channel… |
| `cpp-coding-standards` | C++ coding standards based on the C++ Core Guidelines (isocpp.github.io). Use when writing, reviewing, or refactoring C++ code to enforce… |
| `cpp-testing` | Use only when writing/updating/fixing C++ tests, configuring GoogleTest/CTest, diagnosing failing or flaky tests, or adding coverage/sani… |
| `crosspost` | Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. Adapts content per platform using content-engine patterns.… |
| `csharp-testing` | C# and .NET testing patterns with xUnit, FluentAssertions, mocking, integration tests, and test organization best practices. Use when wri… |
| `customer-billing-ops` | Operate customer billing workflows such as subscriptions, refunds, churn triage, billing-portal recovery, and plan analysis using connect… |
| `customs-trade-compliance` | Codified customs and trade compliance expertise — HS/HTS tariff classification with GRI rules, commercial invoices and entry documentatio… |
| `dart-flutter-patterns` | Production-ready Dart and Flutter patterns covering null safety, immutable state with Freezed, async composition, widget architecture, st… |
| `dashboard-builder` | Build monitoring dashboards that answer real operator questions for Grafana, SigNoz, and similar platforms. Use when turning metrics into… |
| `data-scraper-agent` | Build a fully automated AI-powered data collection agent for any public source — job boards, prices, news, GitHub, sports, anything. Runs… |
| `data-throughput-accelerator` | Diagnose and accelerate large data movement — ingestion, backfill, export, ETL, warehouse loading, manifest catch-up, and table synchroni… |
| `database-migrations` | Safe, reversible database migration patterns: forward-only production changes, expand-contract zero-downtime renames, concurrent indexes,… |
| `deep-research` | Produce cited research reports from multiple web sources using firecrawl and exa MCP tools — plan sub-questions, search and deep-read sou… |
| `deepseek-harness-setup` | Install and operate Everything Claude Code (ECC) on the DeepSeek Harness (DSH): native skill roots (~/.dsh/skills, .agents/skills), the @… |
| `defi-amm-security` | Security checklist for Solidity AMM contracts, liquidity pools, and swap flows. Covers reentrancy, CEI ordering, donation or inflation at… |
| `delivery-gate` | Stop hook that blocks Claude from finishing until quality checks pass. Detects rationalization patterns (surface text heuristics), stale… |
| `deployment-patterns` | Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies, and production readiness chec… |
| `design-system` | Generate a design system from an existing codebase or audit one for visual consistency: extract tokens (colors, typography, spacing, shad… |
| `dev-team` | Simulate a collaborative dev team session where multiple role-based personas (PM, Architect, Developer, QA) respond to the same problem t… |
| `devfleet` | Orchestrate multi-agent coding tasks via Claude DevFleet — plan projects, dispatch parallel agents in isolated worktrees, monitor progres… |
| `django-celery` | Django + Celery async task patterns — configuration, task design, beat scheduling, retries, canvas workflows, monitoring, and testing. Us… |
| `django-patterns` | Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and production-grade Django app… |
| `django-security` | Django security best practices, authentication, authorization, CSRF protection, SQL injection prevention, XSS prevention, and secure depl… |
| `django-tdd` | Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Django REST Framework APIs. Us… |
| `django-verification` | Run the full Django verification loop — environment check, mypy/ruff/black linting, migration safety, pytest with coverage targets, pip-a… |
| `dmux-workflows` | Multi-agent orchestration using dmux (tmux pane manager for AI agents). Patterns for parallel agent workflows across Claude Code, Codex,… |
| `docker-patterns` | Docker and Docker Compose patterns for local development, hardened CLI installer harnesses, container security, networking, volumes, and… |
| `docs-governance` | Route broad documentation-governance requests to existing ECC skills and run an opt-in, read-only audit of mapped documentation roles, li… |
| `documentation-lookup` | Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code… |
| `dotnet-patterns` | Idiomatic C# and .NET patterns, conventions, dependency injection, async/await, and best practices for building robust, maintainable .NET… |
| `dynamic-workflow-mode` | Design task-local harnesses, eval gates, and reusable skill extraction for Claude dynamic workflow mode and other adaptive agent harnesse… |
| `e2e-testing` | Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies. Use… |
| `ecc-contribution-review` | Prepare an ECC skill contribution for review by organizing repository, install-surface, cross-harness, validation, security, and commit o… |
| `ecc-guide` | Answer questions about ECC by reading the live repo surface — agents, skills, commands, hooks, rules, install profiles, and docs — instea… |
| `ecc-recipes` | Map a described workflow to the right ECC command group with run-order and stop condition, or browse all command-group recipe families re… |
| `ecc-tools-cost-audit` | Evidence-first ECC Tools burn and billing audit workflow. Use when investigating runaway PR creation, quota bypass, premium-model leakage… |
| `email-ops` | Evidence-first mailbox triage, drafting, send verification, and sent-mail-safe follow-up workflow for ECC. Use when the user wants to org… |
| `energy-procurement` | Procure electricity and natural gas for commercial and industrial facilities: tariff and rate-schedule optimization, demand-charge mitiga… |
| `enterprise-agent-ops` | Operational controls for long-lived or cloud-hosted agent systems — runtime lifecycle (start, pause, stop, restart), observability (logs,… |
| `error-handling` | Patterns for robust error handling across TypeScript, Python, and Go. Covers typed errors, error boundaries, retries, circuit breakers, a… |
| `esign-field-placement` | Deterministic method for placing signature, date, and text fields in a web e-signature composer through a browser automation session, usi… |
| `eval-harness` | Eval-driven development (EDD) framework for AI coding sessions — define capability and regression evals before coding, grade with code-ba… |
| `evm-token-decimals` | Prevent silent decimal mismatch bugs across EVM chains. Covers runtime decimal lookup, chain-aware caching, bridged-token precision drift… |
| `exa-search` | Neural search via Exa MCP for web, code, and company research. Use when the user needs web search, code examples, company intel, people l… |
| `fal-ai-media` | Unified media generation via fal.ai MCP — image, video, and audio. Covers text-to-image (Nano Banana), text/image-to-video (Seedance, Kli… |
| `fastapi-patterns` | FastAPI best practices covering project structure, Pydantic v2 schemas, dependency injection, async handlers, authentication, authorizati… |
| `finance-billing-ops` | Evidence-first revenue, pricing, refunds, team-billing, and billing-model truth workflow for ECC. Use when the user wants a sales snapsho… |
| `flox-environments` | Create reproducible, cross-platform (macOS/Linux) development environments with Flox, a declarative Nix-based environment manager. Use wh… |
| `flutter-dart-code-review` | Library-agnostic Flutter/Dart code review checklist covering widget best practices, state management patterns (BLoC, Riverpod, Provider,… |
| `foundation-models-on-device` | Apple FoundationModels framework for on-device LLM — text generation, guided generation with @Generable, tool calling, and snapshot strea… |
| `frontend-a11y` | Accessibility patterns for React and Next.js — semantic HTML, ARIA attributes, form labeling, keyboard navigation, focus management, and… |
| `frontend-design-direction` | Set an ECC-specific frontend design direction for production UI work. Use when building or improving websites, dashboards, applications,… |
| `frontend-patterns` | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. Use when building or… |
| `frontend-slides` | Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a pre… |
| `fsharp-testing` | F# testing patterns with xUnit, FsUnit, Unquote, FsCheck property-based testing, integration tests, and test organization best practices.… |
| `gan-style-harness` | GAN-inspired Generator-Evaluator agent harness for building high-quality applications autonomously. Based on Anthropic's March 2026 harne… |
| `gateguard` | PreToolUse fact-forcing gate that denies the first Edit/Write/Bash (including MultiEdit and NotebookEdit) attempt until the agent present… |
| `generating-python-installer` | Commercial-grade Python installer expert for Windows: Nuitka extreme compilation, dist slimming, DLL footprint analysis, and Inno Setup p… |
| `git-workflow` | Git workflow patterns including branching strategies, commit conventions, keeping history clean and readable, tidying local commits befor… |
| `github-ops` | GitHub repository operations, automation, and management. Issue triage, PR management, CI/CD operations, release management, and security… |
| `godot-patterns` | Idiomatic Godot 4 GDScript patterns - static typing, scene and node design, signals, resources, autoloads, input, and lifecycle safety. U… |
| `godot-testing` | Testing Godot 4 GDScript projects - a zero-dependency headless check scene, gdUnit4 and GUT suites, scene-runner tests, signal assertions… |
| `golang-patterns` | Idiomatic Go patterns, best practices, and conventions for building robust, efficient, and maintainable Go applications. Use when writing… |
| `golang-testing` | Go testing patterns including table-driven tests, subtests, benchmarks, fuzzing, and test coverage. Follows TDD methodology with idiomati… |
| `google-workspace-ops` | Operate across Google Drive, Docs, Sheets, and Slides as one workflow surface for plans, trackers, decks, and shared documents. Use when… |
| `growth-log` | Write growth log entries that extract reusable patterns from completed work — root cause, transferable rule, and a recognizable signal —… |
| `healthcare-cdss-patterns` | Clinical Decision Support System (CDSS) development patterns. Drug interaction checking, dose validation, clinical scoring (NEWS2, qSOFA)… |
| `healthcare-emr-patterns` | EMR/EHR development patterns for healthcare applications. Clinical safety, encounter workflows, prescription generation, clinical decisio… |
| `healthcare-eval-harness` | Patient safety evaluation harness for healthcare application deployments. Automated test suites for CDSS accuracy, PHI exposure, clinical… |
| `healthcare-phi-compliance` | Protected Health Information (PHI) and PII compliance patterns for healthcare applications: data classification, row-level access control… |
| `hermes-imports` | Convert local Hermes operator workflows into sanitized ECC skills and release-pack artifacts. Use when preparing a Hermes workflow for pu… |
| `hexagonal-architecture` | Design, implement, and refactor Ports & Adapters systems with clear domain boundaries, dependency inversion, and testable use-case orches… |
| `hipaa-compliance` | HIPAA-specific entrypoint for healthcare privacy and security work. Use when a task is explicitly framed around HIPAA, PHI handling, cove… |
| `homelab-network-readiness` | Readiness checklist for homelab VLAN segmentation, local DNS filtering (Pi-hole, AdGuard Home), and WireGuard-style remote access. Use wh… |
| `homelab-network-setup` | Practical home and homelab network planning for gateways, switches, access points, IP ranges, DHCP reservations, DNS, cabling, and common… |
| `homelab-pihole-dns` | Pi-hole installation, blocklist management, DNS-over-HTTPS setup, DHCP integration, local DNS records, and troubleshooting broken DNS res… |
| `homelab-vlan-segmentation` | Segmenting home networks into VLANs for IoT, guest, trusted, and server traffic using UniFi, pfSense/OPNsense, and MikroTik — including s… |
| `homelab-wireguard-vpn` | WireGuard VPN server setup, peer configuration, key generation, split tunneling vs full tunnel routing, and remote access to a home netwo… |
| `hookify-rules` | Create and configure hookify rules — markdown files with YAML frontmatter that match bash, file, prompt, or stop events by regex or condi… |
| `i18n-sync` | Translate and synchronize application JSON locale files using source-key usage, project terminology, and focused validation. Use when add… |
| `inherit-legacy-style` | Prevent AI style drift on legacy projects by scanning the codebase for implicit conventions, resolving conflicts with the operator one at… |
| `intent-driven-development` | Turn ambiguous or high-impact product and engineering changes into scoped, verifiable acceptance criteria before or alongside implementat… |
| `inventory-demand-planning` | Codified demand planning expertise for multi-location retailers: demand forecasting method selection, ABC/XYZ segmentation, safety stock… |
| `investor-materials` | Create and update pitch decks, one-pagers, investor memos, accelerator applications, financial models, and fundraising materials. Use whe… |
| `investor-outreach` | Draft cold emails, warm intro blurbs, follow-ups, update emails, and investor communications for fundraising. Use when the user wants out… |
| `ios-icon-gen` | Generate iOS app icons as PNG imagesets for Xcode asset catalogs from SF Symbols (5000+ Apple-native) or Iconify API (275k+ open source i… |
| `issue-review` | Review a GitHub issue the way /code-review reviews a PR. Fetches the issue with the gh CLI, checks the report against the current codebas… |
| `iterative-retrieval` | Pattern for progressively refining context retrieval to solve the subagent context problem. Use when a subagent lacks the context it need… |
| `ito-baskets` | Read-only Itô basket and prediction-market data skill. Index the live basket catalog, compare a basket against user-supplied research or… |
| `ito-compute` | Query live GPU inventory, submit an authenticated Itô fixed-rate RFQ, inspect RFQ or procurement status, revoke device credentials, and r… |
| `ito-inference` | Inspect the availability of model serving on a completed Itô compute booking and, when the canonical backend becomes available, hand off… |
| `ito-training` | Inspect the availability of ML training on a completed Itô compute booking and, when the canonical backend becomes available, hand off an… |
| `java-coding-standards` | Java coding standards for Spring Boot and Quarkus services: naming, immutability, Optional usage, streams, exceptions, generics, CDI, rea… |
| `jira-integration` | Retrieves Jira tickets, analyzes requirements, updates ticket status, adds comments, or transitions issues via MCP or direct REST API pat… |
| `jpa-patterns` | JPA/Hibernate patterns for entity design, relationships, query optimization, transactions, auditing, indexing, pagination, and pooling in… |
| `knowledge-ops` | Knowledge base management, ingestion, sync, and retrieval across multiple storage layers (local files, MCP memory, vector stores, Git rep… |
| `kotlin-coroutines-flows` | Kotlin Coroutines and Flow patterns for Android and KMP — structured concurrency, Flow operators, StateFlow, error handling, and testing.… |
| `kotlin-exposed-patterns` | JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repo… |
| `kotlin-ktor-patterns` | Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSockets, and testApplication test… |
| `kotlin-patterns` | Idiomatic Kotlin patterns, best practices, and conventions for building robust, efficient, and maintainable Kotlin applications with coro… |
| `kotlin-testing` | Kotlin testing patterns with Kotest, MockK, coroutine testing, property-based testing, and Kover coverage. Follows TDD methodology with i… |
| `kubernetes-patterns` | Kubernetes workload patterns, resource management, RBAC, probes, autoscaling, ConfigMap/Secret handling, and kubectl debugging for produc… |
| `laravel-patterns` | Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and API resources for producti… |
| `laravel-plugin-discovery` | Discover and evaluate Laravel packages via LaraPlugins.io MCP. Use when the user wants to find plugins, check package health, or assess L… |
| `laravel-security` | Laravel security best practices — authentication, authorization, Eloquent safety, CSRF, XSS prevention, API security, and secure deployme… |
| `laravel-tdd` | Laravel testing strategies with PHPUnit, Pest, model factories, HTTP tests, Sanctum authentication testing, mocking, and coverage. Use wh… |
| `laravel-verification` | Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security scans, and deployment readine… |
| `latency-critical-systems` | Optimize and verify latency-sensitive systems — realtime dashboards, market data feeds, streaming agents, execution gateways, queues, and… |
| `lead-intelligence` | AI-native lead intelligence and outreach pipeline. Replaces Apollo, Clay, and ZoomInfo with agent-powered signal scoring, mutual ranking,… |
| `leanrea` | Reverse engineers shipped software with bounded local CLI inspection. Covers PE headers, Electron archives, custom binary formats, SQLite… |
| `liquid-glass-design` | iOS 26 Liquid Glass design system — dynamic glass material with blur, reflection, and interactive morphing for SwiftUI, UIKit, and Widget… |
| `living-docs-governance` | Keep a long-lived project's documentation from rotting by assigning existing project docs clear constitution, map, status, and history ro… |
| `llm-trading-agent-security` | Security patterns for autonomous trading agents with wallet or transaction authority. Covers prompt injection, spend limits, pre-send sim… |
| `logistics-exception-management` | Codified freight-exception handling expertise for shipment delays, damages, losses, shortages, and carrier disputes, with escalation prot… |
| `loop-design-check` | Design a goal-oriented agent loop or review one for failure modes: spinning, Goodhart-gaming the verifier, or running a wrong answer to c… |
| `mailtrap-email-integration` | Guides agents through integrating transactional email sending via Mailtrap's Email API, including sandbox testing, domain verification, a… |
| `make-interfaces-feel-better` | Apply concrete design-engineering details that make interfaces feel polished. Use when reviewing or improving UI spacing, typography, bor… |
| `manim-video` | Build reusable Manim explainers for technical concepts, graphs, system diagrams, and product walkthroughs, then hand off to the wider ECC… |
| `market-research` | Conduct market research, competitive analysis, investor due diligence, and industry intelligence with source attribution and decision-ori… |
| `marketing-campaign` | End-to-end marketing campaign planning and execution. Covers audience research, positioning, campaign angle definition, landing page copy… |
| `master-agreement-generator` | Generate review drafts of counterparty master agreements from one template plus a JSON spec, with role-selected clauses and a Schedule A… |
| `mcp-dependency-review` | Statically review MCP configuration for mutable package references before approval or CI, without executing discovered MCP servers. Use w… |
| `mcp-server-patterns` | Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs Streamable HTTP. Use Context7 or officia… |
| `messages-ops` | Evidence-first live messaging workflow for ECC. Use when the user wants to read texts or DMs, recover a recent one-time code, inspect a t… |
| `ml-adoption-playbook` | End-to-end methodology for AI agents and software engineers to add machine learning algorithms to existing non-ML codebases. Covers probl… |
| `mle-workflow` | Production machine-learning engineering workflow for data contracts, reproducible training, model evaluation, deployment, monitoring, and… |
| `module-governance` | - Establish or maintain a business module's local agent instructions, domain-context links, and interface ownership when implementing a n… |
| `module-regression` | - Govern cross-module regression in large repositories with a REGRESSION.md ledger that records each module's downstream consumers and ex… |
| `motion-advanced` | Advanced motion patterns for React / Next.js — drag & drop, gestures, text animations, SVG path drawing, custom hooks, imperative sequenc… |
| `motion-foundations` | Motion tokens, spring presets, performance rules, device adaptation, accessibility enforcement, and SSR safety for React / Next.js using… |
| `motion-patterns` | Production-ready animation patterns for React / Next.js — button, modal, toast, stagger, page transitions, exit animations, scroll, and l… |
| `mybatis-patterns` | MyBatis and MyBatis-Spring patterns for mapper design, XML and annotation SQL, result mapping, dynamic SQL safety, transactions, batching… |
| `mysql-patterns` | MySQL and MariaDB schema, query, indexing, transaction, replication, and connection-pool patterns for production backends. Use when desig… |
| `nanoclaw-repl` | Operate and extend NanoClaw, ECC's zero-dependency session-aware REPL, with persistent markdown-backed sessions and slash commands for mo… |
| `nasiko-control-plane` | Manage the experimental Nasiko CLI lifecycle through ECC — read-only status checks, consent-gated install of the pinned qualified version… |
| `nestjs-patterns` | NestJS architecture patterns for modules, controllers, providers, DTO validation, guards, interceptors, config, and production-grade Type… |
| `netmiko-ssh-automation` | Safe Python Netmiko patterns for read-only collection, bounded batch SSH, TextFSM parsing, guarded config changes, timeouts, and network… |
| `network-bgp-diagnostics` | Diagnostics-only BGP troubleshooting patterns for neighbor state, route exchange, prefix policy, AS path inspection, and safe evidence co… |
| `network-config-validation` | Pre-deployment checks for router and switch configuration, including dangerous commands, duplicate addresses, subnet overlaps, stale refe… |
| `network-interface-health` | Diagnose interface errors, drops, CRCs, duplex mismatches, flapping, speed negotiation issues, and counter trends on routers, switches, a… |
| `nextjs-turbopack` | Next.js 16+ and Turbopack guidance — incremental Rust bundling, file-system caching, faster dev startup and HMR, Turbopack vs webpack tra… |
| `nodejs-keccak256` | Prevent Ethereum hashing bugs in JavaScript and TypeScript. Node's sha3-256 is NIST SHA3, not Ethereum Keccak-256, and silently breaks se… |
| `nutrient-document-processing` | Process, convert, OCR, extract, redact, sign, and fill documents using the Nutrient DWS API. Works with PDFs, DOCX, XLSX, PPTX, HTML, and… |
| `nuxt4-patterns` | Nuxt 4 app patterns for hydration safety, performance, route rules, lazy loading, and SSR-safe data fetching with useFetch and useAsyncDa… |
| `openclaw-persona-forge` | 为 OpenClaw AI Agent 锻造完整的龙虾灵魂方案。根据用户偏好或随机抽卡， 输出身份定位、灵魂描述(SOUL.md)、角色化底线规则、名字和头像生图提示词。 如当前环境提供已审核的生图 skill，可自动生成统一风格头像图片。 当用户需要创建、设计或定制 Op… |
| `opensource-pipeline` | Open-source pipeline: fork, sanitize, and package private projects for safe public release. Chains 3 agents (forker, sanitizer, packager)… |
| `osint-investigation` | Sparse-clue OSINT investigation methodology for extracting overlooked leads, connecting fragmented evidence, and testing explanations acr… |
| `parallel-execution-optimizer` | Speed up a task by turning it into a dependency graph of parallel lanes with a lane matrix, batched reads and checks, write surfaces isol… |
| `perl-patterns` | Modern Perl 5.36+ idioms, best practices, and conventions for building robust, maintainable Perl applications. Use when writing or review… |
| `perl-security` | Comprehensive Perl security covering taint mode, input validation, safe process execution, DBI parameterized queries, web security (XSS/S… |
| `perl-testing` | Perl testing patterns using Test2::V0, Test::More, prove runner, mocking, coverage with Devel::Cover, and TDD methodology. Use when writi… |
| `plan-orchestrate` | Read a plan document, decompose it into steps, classify each step, and emit the ready-to-paste ECC slash command for that step, carrying… |
| `plankton-code-quality` | Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude-powered fixes on every file edit via hooks. Use… |
| `platform-factory` | Build deterministic OCI images, SBOM/provenance evidence and hardened container or microVM runs from a compiled executable with the Platf… |
| `postgres-patterns` | PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices. Use when de… |
| `prediction-market-oracle-research` | Research prediction markets as data sources or oracle signals for products, agents, dashboards, and corporate decision intelligence. Use… |
| `prediction-market-risk-review` | Review prediction-market, basket, oracle, and trading-agent workflows for compliance, safety, data-quality, privacy, and execution risk.… |
| `prisma-patterns` | Prisma ORM patterns for TypeScript backends — schema design, query optimization, transactions, pagination, and critical traps like update… |
| `product-capability` | Translate PRD intent, roadmap asks, or product discussions into an implementation-ready capability plan that exposes constraints, invaria… |
| `product-lens` | Validate the why before building through four product diagnostics — a YC-style product diagnostic that produces PRODUCT-BRIEF.md with a g… |
| `production-audit` | Local-evidence production readiness audit for shipped apps, pre-launch reviews, post-merge checks, and "what breaks in prod?" questions w… |
| `production-scheduling` | Codified expertise for production scheduling, job sequencing, line balancing, changeover optimization, and bottleneck resolution in discr… |
| `project-flow-ops` | Operate execution flow across GitHub and Linear by triaging issues and pull requests, linking active work, and keeping GitHub public-faci… |
| `prompt-caching-strategy` | - Optimize LLM prompt caching hit rate to reduce API costs and improve latency. Analyzes prompt structure, identifies cacheable vs non-ca… |
| `prompt-optimizer` | Analyze draft prompts, detect intent and missing context, match ECC commands, skills, and agents, and output a ready-to-paste optimized p… |
| `python-patterns` | Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications. Us… |
| `python-testing` | Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requirements. Use when writing… |
| `pytorch-patterns` | PyTorch deep learning patterns and best practices for building robust, efficient, and reproducible training pipelines, model architecture… |
| `quality-nonconformance` | Quality control and non-conformance management for regulated manufacturing (FDA 21 CFR 820, IATF 16949, AS9100): NCR lifecycle and dispos… |
| `quarkus-patterns` | Quarkus 3.x LTS architecture patterns with Camel for messaging, RESTful API design, CDI services, data access with Panache, and async pro… |
| `quarkus-security` | Quarkus security implementation patterns: JWT and OIDC authentication, @RolesAllowed RBAC and SecurityIdentity checks, Bean Validation an… |
| `quarkus-tdd` | Test-driven development for Quarkus 3.x LTS using JUnit 5, Mockito, REST Assured, Camel testing, and JaCoCo. Use when adding features, fi… |
| `quarkus-verification` | Verification loop for Quarkus projects: build, static analysis (Checkstyle, PMD, SpotBugs), tests with JaCoCo coverage, OWASP dependency… |
| `rails-patterns` | Ruby on Rails framework patterns for Rails 7.1+ and 8.x apps. Covers the directory contract, skinny controllers with service objects, for… |
| `rails-security` | Ruby on Rails security practices for Rails 7.1+ and 8.x apps. Covers production configuration, authentication, authorization, strong para… |
| `ralphinho-rfc-pipeline` | Split an RFC into a multi-agent execution DAG — decompose into work units with dependencies and acceptance tests, run research, plan, imp… |
| `react-native-patterns` | React Native and Expo app patterns — Expo Router navigation, state separation (server/client/route/form), TanStack Query data fetching wi… |
| `react-patterns` | React 18/19 patterns including hooks discipline, server/client component boundaries, Suspense + error boundaries, form actions, data fetc… |
| `react-performance` | React and Next.js performance optimization patterns adapted from Vercel Engineering's React Best Practices (https://github.com/vercel-lab… |
| `react-testing` | React component testing with React Testing Library, Vitest/Jest, MSW for network mocking, accessibility assertions with axe, and the deci… |
| `recsys-pipeline-architect` | Design composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect frame… |
| `recursive-decision-ledger` | Run repeated rollouts ("Prime Gauss" style recursive prompting) while keeping an append-only decision ledger of trials, marks, coherence… |
| `redis-patterns` | Redis data structure patterns, caching strategies, distributed locks, rate limiting, pub/sub, and connection management for production ap… |
| `regex-vs-llm-structured-text` | Decision framework for parsing structured text (quizzes, forms, invoices, receipts, tables) with a hybrid regex-first pipeline — regex ex… |
| `remotion-video-creation` | Best practices for Remotion - Video creation in React. 29 domain-specific rules covering 3D, animations, audio, captions, charts, transit… |
| `repo-scan` | Bootstrap pointer that installs the external repo-scan skill from a pinned, reviewable commit. Use when repo-scan must be installed befor… |
| `research-ops` | Evidence-first current-state research workflow for ECC. Use when the user wants fresh facts, comparisons, enrichment, or a recommendation… |
| `returns-reverse-logistics` | Codified expertise for returns authorization, receipt and inspection, disposition decisions, refund processing, fraud detection, and warr… |
| `roundhouse-x402` | Discover x402-paid services and ERC-8004 agent identity via Roundhouse (open catalog, paid SQL, MCP server, rh-x402 CLI), and optionally… |
| `rules-distill` | Scan skills to extract cross-cutting principles and distill them into rules — append, revise, or create new rule files. Use when the same… |
| `rust-patterns` | Idiomatic Rust patterns, ownership, error handling, traits, concurrency, and best practices for building safe, performant applications. U… |
| `rust-testing` | Rust testing patterns including unit tests, integration tests, async testing, property-based testing, mocking, and coverage. Follows TDD… |
| `safety-guard` | Guard against destructive operations with three modes: Careful intercepts dangerous commands (rm -rf, git push --force, DROP TABLE) for c… |
| `santa-method` | Multi-agent adversarial verification: two independent reviewers with the same rubric must both pass before output ships, with a fix-and-r… |
| `scientific-db-openalex-database` | OpenAlex REST API workflows for cross-disciplinary literature search, DOI/PMID lookup, open-access links, citation counts, and reproducib… |
| `scientific-db-pubmed-database` | Direct PubMed and NCBI E-utilities search workflows for biomedical literature, MeSH queries, PMID lookup, citation retrieval, and API-bac… |
| `scientific-db-uspto-database` | USPTO patent and trademark data workflow for official record lookup, PatentSearch queries, TSDR checks, assignment data, and reproducible… |
| `scientific-pkg-gget` | gget CLI and Python workflow for quick genomic database queries, sequence lookup, BLAST-style searches, enrichment checks, and reproducib… |
| `scientific-thinking-literature-review` | Systematic literature-review workflow for academic, biomedical, technical, and scientific topics, including search planning, source scree… |
| `scientific-thinking-scholar-evaluation` | Structured scholarly-work evaluation for papers, proposals, literature reviews, methods sections, evidence quality, citation support, and… |
| `search-first` | Research-before-coding workflow: search npm/PyPI, MCP servers, skills, and GitHub for existing tools before writing custom code, then ado… |
| `security-bounty-hunter` | Hunt for exploitable, bounty-worthy security issues in repositories. Focuses on remotely reachable vulnerabilities that qualify for real… |
| `security-review` | Security review checklist and patterns for adding authentication, handling user input, managing secrets, creating API endpoints, or imple… |
| `security-scan` | Scan your Claude Code configuration (.claude/ directory) for security vulnerabilities, misconfigurations, and injection risks using Agent… |
| `seo` | Audit, plan, and implement SEO improvements across technical SEO, on-page optimization, structured data, Core Web Vitals, and content str… |
| `short-video-distribution` | Ship a finished vertical video to TikTok, YouTube Shorts, and Instagram Reels. Checks the file against each platform's limits, writes nat… |
| `skill-comply` | Visualize whether skills, rules, and agent definitions are actually followed — auto-generates scenarios at 3 prompt strictness levels, ru… |
| `skill-host-compat` | Lint ECC skills for Codex/Cursor-safe frontmatter and Claude-only substitutions before a skill PR. |
| `skill-scout` | Search existing local, marketplace, GitHub, and web skill sources before creating a new skill. Use when the user wants to create, build,… |
| `skill-stocktake` | Use when auditing Claude skills and commands for quality. Supports Quick Scan (changed skills only) and Full Stocktake modes with sequent… |
| `social-graph-ranker` | Weighted social-graph ranking for warm intro discovery, bridge scoring, and network gap analysis across X and LinkedIn. Use when the user… |
| `social-publisher` | Agent-driven scheduling and publishing of social media posts across 13 platforms via SocialClaw. Use when the user wants to publish to X,… |
| `springboot-patterns` | Spring Boot architecture patterns, REST API design, layered services, data access, caching, async processing, and logging. Use for Java S… |
| `springboot-security` | Spring Security best practices for authn/authz, validation, CSRF, secrets, headers, rate limiting, and dependency security in Java Spring… |
| `springboot-tdd` | Test-driven development for Spring Boot using JUnit 5, Mockito, MockMvc, Testcontainers, and JaCoCo. Use when adding features, fixing bug… |
| `springboot-verification` | Run the full Spring Boot verification loop — Maven or Gradle build, SpotBugs, PMD, and Checkstyle static analysis, unit and Testcontainer… |
| `story-lifecycle` | Manage a file-based epic → story → sprint development loop without requiring an external project management tool. Creates and tracks epic… |
| `strategic-compact` | Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction. Us… |
| `swift-actor-persistence` | Thread-safe data persistence in Swift using actors — in-memory cache with file-backed storage, eliminating data races by design. Use when… |
| `swift-concurrency-6-2` | Swift 6.2 Approachable Concurrency — single-threaded by default, @concurrent for explicit background offloading, isolated conformances fo… |
| `swift-protocol-di-testing` | Protocol-based dependency injection for testable Swift code — mock file system, network, and external APIs using focused protocols and Sw… |
| `swiftui-patterns` | SwiftUI architecture patterns, state management with @Observable, view composition, navigation, performance optimization, and modern iOS/… |
| `taste` | Creative-direction layer for music videos and short-form edits in the angelcore / cloud-trance / hyperpop family — a named-genre aestheti… |
| `taste-application` | Generate new video against a distilled style pack and cut it into a finished piece - plan takes from the reference's cut rhythm, generate… |
| `taste-distillation` | Measure a set of reference videos into a reusable style pack - colour grade as a 3D LUT, cut rhythm as a shot-length distribution, hero s… |
| `tdd-workflow` | Test-driven development workflow: write a failing test first, watch it fail, implement the smallest change to green, then refactor with 8… |
| `team-agent-orchestration` | Run team-based orchestration for agent squads: work items with owners and scope, agent Kanban state, branch isolation, control pane visib… |
| `terminal-opener` | Open an executable and its argument array in a visible terminal window through a reusable, shell-free launch plan with dry-run, JSON, cap… |
| `terminal-ops` | Evidence-first repo execution workflow for ECC. Use when the user wants a command run, a repo checked, a CI failure debugged, or a narrow… |
| `terraform-patterns` | Terraform and OpenTofu infrastructure-as-code patterns for project layout, remote state, modules, variables, secrets, safe plan/apply wor… |
| `test-collaboration` | Inventory and govern a project's test assets. Connect requirements, business rules, risks, bugs, and cross-boundary contracts to stable T… |
| `tinystruct-patterns` | Expert guidance for developing with the tinystruct Java framework. Use when working on the tinystruct codebase or any project built on ti… |
| `token-card` | Render a token-usage stat card from local Claude Code, Codex, Gemini CLI, and OpenCode session logs and commit it into the repository as… |
| `typescript-patterns` | TypeScript patterns for strict, type-safe, maintainable code in modern TypeScript and JavaScript applications. Covers strict compiler con… |
| `ui-demo` | Record polished UI demo videos using Playwright. Use when the user asks to create a demo, walkthrough, screen recording, or tutorial vide… |
| `ui-to-vue` | Use when the user has UI screenshots or design exports that need batch conversion into Vue 3 components, especially with Vant, Element Pl… |
| `uncloud` | Use when managing an Uncloud cluster — deploying services, configuring Caddy ingress, adding static proxy routes for non-cluster devices,… |
| `unified-memory` | Share durable, inspectable context and handoffs between Claude, Codex, Hermes, Cursor, OpenCode, and other agents through the local ECC M… |
| `unified-notifications-ops` | Operate notifications as one ECC-native workflow across GitHub, Linear, desktop alerts, hooks, and connected communication surfaces. Use… |
| `verification-loop` | Run a six-phase verification of a Claude Code session's work — build, type check, lint, tests with coverage, security grep, and diff revi… |
| `video-editing` | AI-assisted video editing workflows for cutting, structuring, and augmenting real footage. Covers the full pipeline from raw capture thro… |
| `videodb` | Ingest, index, search, edit, and monitor video and audio with the VideoDB Python SDK — upload from files, URLs, or RTSP feeds, build spok… |
| `visa-doc-translate` | Translate visa document images (bank deposit, employment, income, and retirement certificates; HEIC, PNG, or JPG) into English via OCR an… |
| `vite-patterns` | Vite build tool patterns including config, plugins, HMR, env variables, proxy setup, SSR, library mode, dependency pre-bundling, and buil… |
| `vue-patterns` | Vue.js 3 Composition API patterns, component architecture, reactivity best practices, Pinia state management, Vue Router navigation, and… |
| `web-perimeter-owasp-2025-audit` | Passive, non-destructive web perimeter security auditing mapped to OWASP Top 10:2025 surface leads, CDN Unkeyed Header Web Cache Poisonin… |
| `windows-desktop-e2e` | E2E testing for Windows native desktop apps (WPF, WinForms, Win32/MFC, Qt) using pywinauto and Windows UI Automation. Use when writing E2… |
| `workspace-surface-audit` | Audit the active repo, MCP servers, plugins, connectors, env surfaces, and harness setup, then recommend the highest-value ECC-native ski… |
| `x-api` | X/Twitter API integration for posting tweets, threads, reading timelines, search, and analytics. Covers OAuth auth patterns, rate limits,… |
| `yoruba-localization-testing` | Test Yoruba (yo) and English bilingual interfaces for tone marks, underdots, Unicode normalization, translation fallback, and accessibility. |

</details>

<details><summary>Agents — plugin `ecc` (72)</summary>

| Nom | Description |
|---|---|
| `a11y-architect` | Accessibility Architect specializing in WCAG 2.2 compliance for Web and Native platforms. Use PROACTIVELY when designing UI components, e… |
| `agent-evaluator` | Evaluates agent output against 5-axis quality rubric (accuracy, completeness, clarity, actionability, conciseness). Use after any non-tri… |
| `architect` | Software architecture specialist for system design, scalability, and technical decision-making. Use PROACTIVELY when planning new feature… |
| `bengali-reviewer` | Reviews code handling Bengali (Bangla) text for Unicode correctness, proper normalization, script-aware processing, and internationalizat… |
| `build-error-resolver` | Build and TypeScript error resolution specialist. Use PROACTIVELY when build fails or type errors occur. Fixes build/type errors only wit… |
| `chief-of-staff` | Personal communication chief of staff that triages email, Slack, LINE, and Messenger. Classifies messages into 4 tiers (skip/info_only/me… |
| `code-architect` | Designs feature architectures by analyzing existing codebase patterns and conventions, then providing implementation blueprints with conc… |
| `code-explorer` | Deeply analyzes existing codebase features by tracing execution paths, mapping architecture layers, and documenting dependencies to infor… |
| `code-reviewer` | Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modi… |
| `code-simplifier` | Simplifies and refines code for clarity, consistency, and maintainability while preserving behavior. Focus on recently modified code unle… |
| `comment-analyzer` | Analyze code comments for accuracy, completeness, maintainability, and comment rot risk. |
| `commit-reviewer` | Reviews a staged diff and drafts a Conventional Commits-compliant message matching the repository's actual history norms. Use before comm… |
| `conversation-analyzer` | Use this agent when analyzing conversation transcripts to find behaviors worth preventing with hooks. Triggered by /hookify without argum… |
| `cpp-build-resolver` | C++ build, CMake, and compilation error resolution specialist. Fixes build errors, linker issues, and template errors with minimal change… |
| `cpp-reviewer` | Expert C++ code reviewer specializing in memory safety, modern C++ idioms, concurrency, and performance. Use for all C++ code changes. MU… |
| `csharp-reviewer` | Expert C# code reviewer specializing in .NET conventions, async patterns, security, nullable reference types, and performance. Use for al… |
| `dart-build-resolver` | Dart/Flutter build, analysis, and dependency error resolution specialist. Fixes `dart analyze` errors, Flutter compilation failures, pub… |
| `database-reviewer` | PostgreSQL database specialist for query optimization, schema design, security, and performance. Use PROACTIVELY when writing SQL, creati… |
| `django-build-resolver` | Django/Python build, migration, and dependency error resolution specialist. Fixes pip/Poetry errors, migration conflicts, import errors,… |
| `django-reviewer` | Expert Django code reviewer specializing in ORM correctness, DRF patterns, migration safety, security misconfigurations, and production-g… |
| `doc-updater` | Documentation and codemap specialist. Use PROACTIVELY for updating codemaps and documentation. Generates docs/CODEMAPS/*, updates READMEs… |
| `docs-lookup` | When the user asks how to use a library, framework, or API or needs up-to-date code examples, use Context7 MCP to fetch current documenta… |
| `e2e-runner` | End-to-end testing specialist using Vercel Agent Browser (preferred) with Playwright fallback. Use PROACTIVELY for generating, maintainin… |
| `fastapi-reviewer` | Reviews FastAPI applications for async correctness, dependency injection, Pydantic schemas, security, OpenAPI quality, testing, and produ… |
| `flutter-reviewer` | Flutter and Dart code reviewer. Reviews Flutter code for widget best practices, state management patterns, Dart idioms, performance pitfa… |
| `fsharp-reviewer` | Expert F# code reviewer specializing in functional idioms, type safety, pattern matching, computation expressions, and performance. Use f… |
| `gan-evaluator` | GAN Harness — Evaluator agent. Tests the live running application via Playwright, scores against rubric, and provides actionable feedback… |
| `gan-generator` | GAN Harness — Generator agent. Implements features according to the spec, reads evaluator feedback, and iterates until quality threshold… |
| `gan-planner` | GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features, sprints, evaluation criteria, and… |
| `gdscript-reviewer` | Expert GDScript and Godot 4 code reviewer specializing in static typing, scene and node design, signals, lifecycle safety, resources, and… |
| `go-build-resolver` | Go build, vet, and compilation error resolution specialist. Fixes build errors, go vet issues, and linter warnings with minimal changes.… |
| `go-reviewer` | Expert Go code reviewer specializing in idiomatic Go, concurrency patterns, error handling, and performance. Use for all Go code changes.… |
| `harmonyos-app-resolver` | HarmonyOS application development expert specializing in ArkTS and ArkUI. Reviews code for V2 state management compliance, Navigation rou… |
| `harness-optimizer` | Improve local agent-harness configuration reliability and cost using eval-driven grading (pass@k/pass^k) derived from the eval-harness sk… |
| `healthcare-reviewer` | Reviews healthcare application code for clinical safety, CDSS accuracy, PHI compliance, and medical data integrity. Specialized for EMR/E… |
| `homelab-architect` | Designs home and small-lab network plans from hardware inventory, goals, and operator experience level, with safe staged changes and roll… |
| `java-build-resolver` | Java/Maven/Gradle build, compilation, and dependency error resolution specialist. Automatically detects Spring Boot or Quarkus and applie… |
| `java-reviewer` | Expert Java code reviewer for Spring Boot and Quarkus projects. Automatically detects the framework and applies the appropriate review ru… |
| `kotlin-build-resolver` | Kotlin/Gradle build, compilation, and dependency error resolution specialist. Fixes build errors, Kotlin compiler errors, and Gradle issu… |
| `kotlin-reviewer` | Kotlin and Android/KMP code reviewer. Reviews Kotlin code for idiomatic patterns, coroutine safety, Compose best practices, clean archite… |
| `loop-operator` | Operate autonomous agent loops, monitor progress, and intervene safely when loops stall. |
| `marketing-agent` | Marketing strategist and copywriter for campaign planning, audience research, positioning, copy creation, and content review. Covers land… |
| `mle-reviewer` | Production machine-learning engineering reviewer for data contracts, feature pipelines, training reproducibility, offline/online evaluati… |
| `network-architect` | Designs enterprise or multi-site network architecture from requirements, using existing network skills for focused routing, validation, a… |
| `network-config-reviewer` | Reviews router and switch configurations for security, correctness, stale references, risky change-window commands, and missing operation… |
| `network-troubleshooter` | Diagnoses network connectivity, routing, DNS, interface, and policy symptoms with a read-only OSI-layer workflow and evidence-backed root… |
| `opensource-forker` | Fork any project for open-sourcing. Copies files, strips secrets and credentials (20+ patterns), replaces internal references with placeh… |
| `opensource-packager` | Generate complete open-source packaging for a sanitized project. Produces CLAUDE.md, setup.sh, README.md, LICENSE, CONTRIBUTING.md, and G… |
| `opensource-sanitizer` | Verify an open-source fork is fully sanitized before release. Scans for leaked secrets, PII, internal references, and dangerous files usi… |
| `performance-optimizer` | Performance analysis and optimization specialist. Use PROACTIVELY for identifying bottlenecks, optimizing slow code, reducing bundle size… |
| `php-reviewer` | Expert PHP code reviewer specializing in PSR-12 compliance, PHP type system, Eloquent ORM patterns, security, and performance. Use for al… |
| `planner` | Expert planning specialist for complex features and refactoring. Use PROACTIVELY when users request feature implementation, architectural… |
| `pr-test-analyzer` | Review pull request test coverage quality and completeness, with emphasis on behavioral coverage and real bug prevention. |
| `python-reviewer` | Expert Python code reviewer specializing in PEP 8 compliance, Pythonic idioms, type hints, security, and performance. Use for all Python… |
| `pytorch-build-resolver` | PyTorch runtime, CUDA, and training error resolution specialist. Fixes tensor shape mismatches, device errors, gradient issues, DataLoade… |
| `rag-pipeline-reviewer` | Reviews RAG (Retrieval-Augmented Generation) pipelines for retrieval quality, chunking strategy, embedding choices, and evaluation covera… |
| `react-build-resolver` | Diagnose and fix React build failures across Vite, webpack, Next.js, CRA, Parcel, esbuild, and Bun. Handles JSX/TSX compile errors, hydra… |
| `react-reviewer` | Expert React/JSX code reviewer specializing in hook correctness, render performance, server/client component boundaries, accessibility, a… |
| `refactor-cleaner` | Dead code cleanup and consolidation specialist. Use PROACTIVELY for removing unused code, duplicates, and refactoring. Runs analysis tool… |
| `ruby-reviewer` | Expert Ruby and Rails code reviewer specializing in idiomatic Ruby, Active Record query safety, Rails security defaults, and RSpec/Minite… |
| `rust-build-resolver` | Rust build, compilation, and dependency error resolution specialist. Fixes cargo build errors, borrow checker issues, and Cargo.toml prob… |
| `rust-reviewer` | Expert Rust code reviewer specializing in ownership, lifetimes, error handling, unsafe usage, and idiomatic patterns. Use for all Rust co… |
| `security-reviewer` | Security vulnerability detection and remediation specialist. Use PROACTIVELY after writing code that handles user input, authentication,… |
| `seo-specialist` | SEO specialist for technical SEO audits, on-page optimization, structured data, Core Web Vitals, and content/keyword mapping. Use for sit… |
| `silent-failure-hunter` | Review code for silent failures, swallowed errors, bad fallbacks, and missing error propagation. |
| `spec-miner` | Extracts behavioral specs from existing codebases for OpenSpec. Produces flat Requirement and Invariant blocks with structured metadata (… |
| `swift-build-resolver` | Swift/Xcode build, compilation, and dependency error resolution specialist. Fixes swift build errors, Xcode build failures, SPM dependenc… |
| `swift-reviewer` | Expert Swift code reviewer specializing in protocol-oriented design, value semantics, ARC memory management, Swift Concurrency, and idiom… |
| `tdd-guide` | Test-Driven Development specialist enforcing write-tests-first methodology. Use PROACTIVELY when writing new features, fixing bugs, or re… |
| `type-design-analyzer` | Analyze type design for encapsulation, invariant expression, usefulness, and enforcement. |
| `typescript-reviewer` | Expert TypeScript/JavaScript code reviewer specializing in type safety, async correctness, Node/web security, and idiomatic patterns. Use… |
| `vue-reviewer` | Expert Vue.js code reviewer specializing in Composition API correctness, reactivity pitfalls, component architecture, template security,… |

</details>

<details><summary>Commandes — plugin `ecc` (91)</summary>

| Nom | Description |
|---|---|
| `add-language-rules` | Workflow command scaffold for add-language-rules in ECC. |
| `aside` | Answer a quick side question without interrupting or losing context from the current task. Resume work automatically after answering. |
| `astra-review` | Send Claude-written code to GPT-6-Astra (ChatGPT, via Codex CLI) for an independent cross-provider review, then fix what it finds. |
| `auto-update` | Pull the latest ECC repo changes and reinstall the current managed targets. |
| `build-fix` | Detect the project build system and incrementally fix build/type errors with minimal safe changes. |
| `checkpoint` | Create, verify, or list workflow checkpoints after running verification checks. |
| `code-review` | Code review — local uncommitted changes or GitHub PR (pass PR number/URL for PR mode). Use for a step-by-step PRP-style checklist review;… |
| `cost-report` | Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for a terminal summary or CSV export of tracked spend… |
| `cpp-build` | Fix C++ build errors, CMake issues, and linker problems incrementally. Invokes the cpp-build-resolver agent for minimal, surgical fixes. |
| `cpp-review` | Comprehensive C++ code review for memory safety, modern C++ idioms, concurrency, and security. Invokes the cpp-reviewer agent. |
| `cpp-test` | Enforce TDD workflow for C++. Write GoogleTest tests first, then implement. Verify coverage with gcov/lcov. |
| `database-migration` | Workflow command scaffold for database-migration in ECC. |
| `ecc-guide` | Navigate ECC's current agents, skills, commands, hooks, install profiles, and docs from the live repository surface. This is the slash-co… |
| `epic-claim` | Claim an epic issue, stamp coordination state, and sync local ownership. |
| `epic-decompose` | Break an epic into task children without creating task branches. |
| `epic-publish` | Publish a validated epic update back to the issue and local cache. |
| `epic-review` | Mark epic review requested, approved, or changes requested. |
| `epic-sync` | Sync epic issue bodies, labels, and local coordination snapshots from GitHub. |
| `epic-unblock` | Sweep blocked epic issues and reopen anything whose dependencies are closed. |
| `epic-validate` | Validate epic readiness, dependencies, and coordination policy. |
| `evolve` | Analyze instincts and suggest or generate evolved structures |
| `fastapi-review` | Review a FastAPI application for architecture, async correctness, dependency injection, Pydantic schemas, security, performance, and test… |
| `feature-dev` | Guided feature development with codebase understanding and architecture focus |
| `feature-development` | Workflow command scaffold for feature-development in ECC. |
| `flutter-build` | Fix Dart analyzer errors and Flutter build failures incrementally. Invokes the dart-build-resolver agent for minimal, surgical fixes. |
| `flutter-review` | Review Flutter/Dart code for idiomatic patterns, widget best practices, state management, performance, accessibility, and security. Invok… |
| `flutter-test` | Run Flutter/Dart tests, report failures, and incrementally fix test issues. Covers unit, widget, golden, and integration tests. |
| `gan-build` | Run a generator/evaluator build loop for implementation tasks with bounded iterations and scoring. |
| `gan-design` | Run a generator/evaluator design loop for frontend or visual work with bounded iterations and scoring. |
| `go-build` | Fix Go build errors, go vet warnings, and linter issues incrementally. Invokes the go-build-resolver agent for minimal, surgical fixes. |
| `go-review` | Comprehensive Go code review for idiomatic patterns, concurrency safety, error handling, and security. Invokes the go-reviewer agent. |
| `go-test` | Enforce TDD workflow for Go. Write table-driven tests first, then implement. Verify 80%+ coverage with go test -cover. |
| `gradle-build` | Fix Gradle build errors for Android and KMP projects |
| `harness-audit` | Run a deterministic repository harness audit and return a prioritized scorecard. Use for a deterministic overall repo-readiness scorecard… |
| `hookify` | Create hooks to prevent unwanted behaviors from conversation analysis or explicit instructions. Use to generate a new hook rule file from… |
| `hookify-help` | Get help with the hookify system |
| `hookify-list` | List all configured hookify rules |
| `instinct-export` | Export instincts from project/global scope to a file |
| `instinct-import` | Import instincts from file or URL into project/global scope |
| `instinct-status` | Show learned instincts (project + global) with confidence |
| `issue-review` | Review a GitHub issue the way /code-review reviews a PR — verify the report against the codebase, find duplicates and prior fixes, score… |
| `jira` | Retrieve a Jira ticket, analyze requirements, update status, or add comments. Uses the jira-integration skill and MCP or REST API. |
| `kotlin-build` | Fix Kotlin/Gradle build errors, compiler warnings, and dependency issues incrementally. Invokes the kotlin-build-resolver agent for minim… |
| `kotlin-review` | Comprehensive Kotlin code review for idiomatic patterns, null safety, coroutine safety, and security. Invokes the kotlin-reviewer agent. |
| `kotlin-test` | Enforce TDD workflow for Kotlin. Write Kotest tests first, then implement. Verify 80%+ coverage with Kover. |
| `learn` | Extract reusable patterns from the current session and save them as candidate skills or guidance. Use to review a session on demand and p… |
| `learn-eval` | Extract reusable patterns from the session, self-evaluate quality before saving, and determine the right save location (Global vs Project). |
| `loop-start` | Prepare a managed autonomous loop pattern with safety defaults and explicit stop conditions, then print the commands to launch and monito… |
| `loop-status` | Inspect active loop state, progress, failure signals, and recommended intervention. |
| `marketing-campaign` | Plan and execute a full marketing campaign. Accepts a product brief and returns positioning, landing page copy, email sequence, social po… |
| `model-route` | Recommend the best model tier for the current task based on complexity, risk, and budget. |
| `multi-backend` | Run a backend-focused multi-model workflow for APIs, algorithms, data, and business logic. |
| `multi-execute` | Execute a multi-model implementation plan while preserving Claude as the only filesystem writer. |
| `multi-frontend` | Run a frontend-focused multi-model workflow for components, layouts, animation, and UI polish. |
| `multi-plan` | Create a multi-model (Codex + Antigravity) implementation plan without modifying production code. Requires the external ccg-workflow runt… |
| `multi-workflow` | Run a full multi-model development workflow with research, planning, execution, optimization, and review. |
| `orch-review` | Run the orch-review native Workflow over a diff (local changes or a GitHub PR) and report blocking vs advisory findings. Surface for the… |
| `pm2` | Analyze a project and generate PM2 service commands for detected frontend, backend, or database services. |
| `pr` | Create a GitHub PR from current branch with unpushed commits — discovers templates, analyzes changes, pushes |
| `project-init` | Detect a project's stack and produce a dry-run ECC onboarding plan using the repository's install manifests and stack mappings. Use to on… |
| `projects` | List known projects and their instinct statistics |
| `promote` | Promote project-scoped instincts to global scope |
| `prp-commit` | Quick commit with natural language file targeting — describe what to commit in plain English |
| `prp-implement` | Execute an implementation plan with rigorous validation loops |
| `prp-plan` | Create comprehensive feature implementation plan with codebase analysis and pattern extraction |
| `prp-pr` | Alias of /pr for the PRP workflow series. Use when creating a pull request mid-PRP workflow; otherwise use /pr. |
| `prune` | Delete pending instincts older than 30 days that were never promoted. Thin CLI wrapper for continuous-learning-v2's instinct-cli.py prune… |
| `python-review` | Comprehensive Python code review for PEP 8 compliance, type hints, security, and Pythonic idioms. Invokes the python-reviewer agent. |
| `quality-gate` | Run the ECC formatter quality gate for a single file and report remediation steps. |
| `react-build` | Fix React build failures (Vite, webpack, Next.js, CRA, Parcel, esbuild, Bun) incrementally — JSX/TSX compile errors, hydration mismatches… |
| `react-review` | Comprehensive React/JSX code review for hook correctness, render performance, server/client component boundaries, accessibility, and Reac… |
| `react-test` | Enforce TDD workflow for React. Write React Testing Library tests first (behavior-focused, accessibility-first), then implement component… |
| `refactor-clean` | Safely identify and remove dead code with verification after each change. |
| `resume-session` | Load the most recent session file from ~/.claude/session-data/ and resume work with full context from where the last session ended. |
| `review-pr` | Comprehensive PR review using specialized agents (code-reviewer, comment-analyzer, pr-test-analyzer, silent-failure-hunter, type-design-a… |
| `rust-build` | Fix Rust build errors, borrow checker issues, and dependency problems incrementally. Invokes the rust-build-resolver agent for minimal, s… |
| `rust-review` | Comprehensive Rust code review for ownership, lifetimes, error handling, unsafe usage, and idiomatic patterns. Invokes the rust-reviewer… |
| `rust-test` | Enforce TDD workflow for Rust. Write tests first, then implement. Verify 80%+ coverage with cargo-llvm-cov. |
| `santa-loop` | Adversarial dual-review convergence loop — two independent model reviewers must both approve before code ships. Use for the CLI-driven ve… |
| `save-session` | Save current session state to a dated file in ~/.claude/session-data/ so work can be resumed in a future session with full context. |
| `security-scan` | Run AgentShield against agent, hook, MCP, permission, and secret surfaces. This is the slash-command entrypoint for that audit; prefer th… |
| `sessions` | Manage Claude Code session history, aliases, and session metadata. |
| `setup-pm` | Configure your preferred package manager (npm/pnpm/yarn/bun) |
| `skill-create` | Analyze local git history to extract coding patterns and generate SKILL.md files. Local version of the Skill Creator GitHub App. Use to g… |
| `skill-health` | Show skill portfolio health dashboard with charts and analytics. Use for the quantitative usage/success-rate dashboard; for a qualitative… |
| `skill-host-compat` | Lint ECC skills for Codex/Cursor-safe frontmatter and Claude-only substitutions before a skill PR. |
| `test-coverage` | Analyze coverage, identify gaps, and generate missing tests toward the target threshold. |
| `token-card` | Render a token-usage stat card from local agent session logs and commit it to the repo. Invokes the token-card skill. |
| `update-codemaps` | Scan project structure and generate token-lean architecture codemaps. |
| `update-docs` | Sync documentation from source-of-truth files such as scripts, schemas, routes, and exports. |
| `vue-review` | Comprehensive Vue.js code review for Composition API correctness, reactivity, composable patterns, template security, accessibility, and… |

</details>

<details><summary>Skills — plugin `instagram-agent` (13)</summary>

| Nom | Description |
|---|---|
| `ig-audit` | - Post-mortem on what the user has already posted - which reels actually worked, why, and what to stop making. Use when the user pastes t… |
| `ig-caption` | - Write the Instagram caption - the line that survives the "... more" cut, the body, the single ask, the search terms and the three hasht… |
| `ig-carousel` | - Build an Instagram carousel - the cover that earns the swipe, slide-by-slide copy, and the 1080x1350 files to upload. Use when the user… |
| `ig-comment` | - Write comments on other people's Instagram posts and reels that read as a person with an opinion, not a bot. Use when the user pastes a… |
| `ig-dm` | - Write Instagram DMs that get replies - the keyword delivery, the first message to someone who engaged, the collab pitch, and the two fo… |
| `ig-human` | - Strip the machine fingerprint out of any draft - em dashes, AI slop words, invisible watermark characters - and score it against a five… |
| `ig-plan` | - Build the week on Instagram - what to post, which format, when, and who to engage with. Use when the user says "plan my week", "what sh… |
| `ig-profile` | - Score an Instagram profile out of 100 against a 12-part rubric and rewrite the parts that lose points - name field, bio, link, highligh… |
| `ig-reel` | - Write an Instagram Reel from a raw idea - hook options off 26 formulas, the spoken script, the on-screen text, and a timed beat sheet -… |
| `ig-reply` | - Handle the comments under the user's own reels and posts - draft replies to the ones worth answering, sorted by which ones are. Use whe… |
| `ig-repurpose` | - Turn one long asset - a YouTube video, podcast, livestream, newsletter, blog post or client call - into a week of reels and carousels.… |
| `ig-story` | - Write the day's Instagram Stories - the frame-by-frame sequence, which stickers to use where, and the one that moves people into the DM… |
| `ig-viral` | - Go and find the reels that are actually working right now in the user's niche, rank them by how far each beat its own account, name the… |

</details>

<details><summary>Skills — plugin `mattpocock-skills` (28)</summary>

| Nom | Description |
|---|---|
| `ask-matt` | Ask which skill or flow fits your situation. A router over the skills in this repo. |
| `chief-of-staff` | Delegate the work to fresh subagents and remember what it taught you in a dated wiki, so the next session picks up the thread. |
| `claude-handoff` | Hand the current conversation off to a fresh background agent that picks up the work immediately. |
| `code-review` | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's d… |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportuni… |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/thr… |
| `domain-modeling` | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or e… |
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user… |
| `handoff` | Compact the current conversation into a handoff document for another agent to pick up. |
| `implement` | Implement a piece of work based on a spec or set of tickets. |
| `implement-spec` | Implement the result of /to-spec and /to-tickets in code. |
| `migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tes… |
| `pr` | Use when writing a PR body. |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels rig… |
| `research` | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user want… |
| `retro` | Conduct a retrospective on a coding session. |
| `scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffol… |
| `software-factory` | Shared language for designing a software factory: the tasks it runs and the services it plugs into. |
| `tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integr… |
| `teach` | Teach the user a new skill or concept, within this workspace. |
| `to-spec` | Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've alread… |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the… |
| `wait-what` | Stop. That last message did not land: re-pitch it. |
| `wayfinder` | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve t… |
| `writing-beats` | Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on it. |
| `writing-for-agents` | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. |
| `writing-fragments` | Writing, explore: mine raw fragments, no structure yet. |
| `writing-shape` | Writing, exploit: shape raw material into an article, paragraph by paragraph. |

</details>

<details><summary>Skills — plugin `ponytail` (5)</summary>

| Nom | Description |
|---|---|
| `ponytail-audit` | Quality audit of a whole repo: bugs, security holes, what breaks under real load, risky code without tests, slow paths, and what to delet… |
| `ponytail-debt` | List every `shortcut:` comment (and older `ponytail:` ones) as a debt ledger. One-shot report, changes nothing. Use for "ponytail debt",… |
| `ponytail-gain` | Show ponytail's measured savings (code, cost, speed) from the benchmark. One-shot display. Use for /ponytail-gain, "what does ponytail sa… |
| `ponytail-help` | Quick reference for ponytail levels, skills and commands. One-shot display. Use for /ponytail-help, "ponytail help", "how do I use ponyta… |
| `ponytail-review` | Quality review of a change: is the logic right, is it safe, does it hold under real load, is risky code tested, is it fast enough, and is… |

</details>

<details><summary>Skills — plugin `superpowers` (12)</summary>

| Nom | Description |
|---|---|
| `diagnosing-superpowers` | Use when a superpowers session went wrong and your human partner wants to know why — repeated work, ignored plans, stumbles, poor results… |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| `executing-plans` | Use when executing an implementation plan in the current session as the implementer yourself — your human partner chose inline execution,… |
| `receiving-code-review` | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionabl… |
| `requesting-code-review` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| `test-driven-development` | Use when implementing any feature or bugfix, before writing implementation code |
| `using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated… |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands a… |
| `writing-plans` | Use when you have a spec or requirements for a multi-step task, before touching code |
| `writing-skills` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |

</details>

<details><summary>Skills — plugin `taste-skill` (1)</summary>

| Nom | Description |
|---|---|
| `design-taste-frontend` | - tasteskill 2.5.1, the anti-slop frontend skill. Builds professional company websites at the level of figma.com and x.ai: plain copy in… |

</details>

<details><summary>Skills — plugin `unslop` (1)</summary>

| Nom | Description |
|---|---|
| `unslop` | Turns vibecoded, AI-looking UI into a designed interface with its own character. Finds a direction from the product itself, then fixes sp… |

</details>

<!-- LISTE:END -->
