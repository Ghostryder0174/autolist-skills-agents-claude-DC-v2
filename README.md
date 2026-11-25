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
