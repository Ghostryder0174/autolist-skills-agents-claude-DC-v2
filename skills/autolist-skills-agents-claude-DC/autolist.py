"""autolist-skills-agents-claude-DC: UserPromptSubmit hook.

Reads only frontmatter (name, description) of installed skills, agents and
plugin commands, caches them in index.json, rebuilds only when the install
changes, then prints a short routing line for the current prompt.
"""
import hashlib, json, math, os, re, sys, unicodedata

HOME = os.path.expanduser("~/.claude")
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HOME, "cache", "autolist")
INDEX = os.path.join(CACHE, "index.json")
CLASSES = os.path.join(HERE, "classes.json")
TOP = 4
MIN_SCORE = 4.0

# French request words -> English words used in skill descriptions.
FR = {
    "site": "website", "page": "page", "accueil": "landing", "bug": "bug", "erreur": "error",
    "corrige": "fix", "corriger": "fix", "repare": "fix", "securite": "security", "faille": "vulnerability",
    "deployer": "deploy", "deploie": "deploy", "mettre": "", "ligne": "", "publier": "publish",
    "video": "video", "montage": "editing", "image": "image", "photo": "image", "logo": "logo",
    "test": "test", "tests": "tests", "revue": "review", "relire": "review", "relis": "review",
    "animation": "animation", "animer": "animate", "design": "design", "maquette": "mockup",
    "commit": "commit", "pousser": "push", "github": "github", "depot": "repo", "documentation": "docs",
    "doc": "docs", "readme": "readme", "pdf": "pdf", "excel": "xlsx", "tableur": "spreadsheet",
    "diapo": "slides", "presentation": "slides", "word": "docx", "planifier": "plan", "plan": "plan",
    "fonctionnalite": "feature", "refactoriser": "refactor", "nettoyer": "cleanup", "lent": "performance",
    "performance": "performance", "vitesse": "speed", "referencement": "seo", "seo": "seo",
    "instagram": "instagram", "tiktok": "tiktok", "youtube": "youtube", "linkedin": "linkedin",
    "publication": "post", "legende": "caption", "carrousel": "carousel", "reel": "reel",
    "marketing": "marketing", "email": "email", "mail": "email", "texte": "copy", "rediger": "writing",
    "ecrire": "writing", "navigateur": "browser", "capture": "screenshot", "ecran": "screenshot",
    "scraper": "scrape", "base": "database", "donnees": "data", "graphique": "chart", "tableau": "dashboard",
    "audit": "audit", "architecture": "architecture", "concurrent": "competitor", "prix": "pricing",
    "application": "app", "mobile": "mobile", "iphone": "ios", "bureau": "desktop", "fenetre": "window",
    "recherche": "research", "chercher": "search", "debug": "debug", "debogage": "debugging",
    "anime": "animate", "animation": "animation", "modale": "modal", "composant": "component",
    "rendu": "render", "plante": "crash", "fonction": "function", "transition": "transition",
    "geste": "gesture", "glisser": "drag", "formulaire": "form", "connexion": "auth", "facture": "billing",
}
STOP = set("""the and for with use when this that from into your you are any not only all its can
les des une pour avec dans sur que qui est pas par plus mon mes ton tes son ses nos vos leur
fait faire moi toi elle nous vous ils sont cette ces aux du de la le un et ou en au je tu il
skill skills agent agents user users use used using code""".split())


def words(text):
    t = unicodedata.normalize("NFKD", text.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return [w for w in re.findall(r"[a-z0-9][a-z0-9+#.]{2,}", t) if w not in STOP]


def front(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            if f.readline().strip() != "---":
                return {}
            data, key = {}, None
            for _ in range(60):
                line = f.readline()
                if not line or line.strip() == "---":
                    break
                m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line.rstrip("\n"))
                if m:
                    key = m.group(1)
                    data[key] = m.group(2).strip().strip("\"'>|")
                elif key and line[:1] in (" ", "\t"):
                    data[key] = (data[key] + " " + line.strip()).strip()
            return data
    except OSError:
        return {}


def plugins():
    try:
        with open(os.path.join(HOME, "plugins", "installed_plugins.json"), encoding="utf-8") as f:
            raw = json.load(f).get("plugins", {})
    except (OSError, ValueError):
        return []
    try:
        with open(os.path.join(HOME, "settings.json"), encoding="utf-8") as f:
            enabled = json.load(f).get("enabledPlugins", {})
    except (OSError, ValueError):
        enabled = {}
    out = []
    for key, entries in raw.items():
        if entries and enabled.get(key, True):
            path = entries[-1].get("installPath")
            if path and os.path.isdir(path):
                out.append((key.split("@")[0], path))
    return out


def signature():
    parts = []
    for p in (os.path.join(HOME, "plugins", "installed_plugins.json"),
              os.path.join(HOME, "settings.json"), os.path.join(HOME, "skills"),
              os.path.join(HOME, "agents"), CLASSES):
        try:
            parts.append(f"{p}:{os.stat(p).st_mtime_ns}")
        except OSError:
            pass
    for d in (os.path.join(HOME, "skills"), os.path.join(HOME, "agents")):
        if os.path.isdir(d):
            for n in os.listdir(d):
                f = os.path.join(d, n, "SKILL.md") if d.endswith("skills") else os.path.join(d, n)
                try:
                    parts.append(f"{n}:{os.stat(f).st_mtime_ns}")
                except OSError:
                    pass
    return hashlib.sha1("|".join(sorted(parts)).encode()).hexdigest()


def scan():
    items = []

    def add(kind, ident, path):
        d = front(path)
        if d:
            items.append({"id": ident(d.get("name")), "kind": kind,
                          "desc": d.get("description", "")[:300]})

    sk = os.path.join(HOME, "skills")
    if os.path.isdir(sk):
        for n in sorted(os.listdir(sk)):
            p = os.path.join(sk, n, "SKILL.md")
            if os.path.isfile(p):
                add("skill", lambda nm, n=n: nm or n, p)
    ag = os.path.join(HOME, "agents")
    if os.path.isdir(ag):
        for f in sorted(os.listdir(ag)):
            if f.endswith(".md"):
                add("agent", lambda nm, f=f: nm or f[:-3], os.path.join(ag, f))
    skip = {"node_modules", ".git", "tests", "test", "docs", "examples", "benchmarks", "i18n"}
    for plug, root in plugins():
        for dp, dn, fn in os.walk(root):
            dn[:] = [x for x in dn if x not in skip]
            rel = os.path.relpath(dp, root).replace("\\", "/")
            if "SKILL.md" in fn and rel.startswith(("skills/", ".claude/skills/")):
                base = os.path.basename(dp)
                add("skill", lambda nm, b=base: f"{plug}:{nm or b}", os.path.join(dp, "SKILL.md"))
            elif rel in ("agents", "commands", ".claude/agents", ".claude/commands"):
                kind = "agent" if rel.endswith("agents") else "command"
                for f in fn:
                    if f.endswith(".md"):
                        add(kind, lambda nm, f=f: f"{plug}:{nm or f[:-3]}", os.path.join(dp, f))
    seen, uniq = set(), []
    for it in items:
        if it["id"] not in seen:
            seen.add(it["id"])
            uniq.append(it)
    return uniq


DEMAND_RX = re.compile(r"interview|grill|questionnaire|interactive|wizard|wait for user|"
                       r"user confirm|back-and-forth|collect .*feedback|asks? the user|setup wizard", re.I)
START_RX = re.compile(r"always[- ]on|every (session|prompt|response|turn)|response (mode|style)|"
                      r"model rout|before any response", re.I)


def short(i):
    return i.split(":")[-1]


def load_classes():
    try:
        with open(CLASSES, encoding="utf-8") as f:
            c = json.load(f)
    except (OSError, ValueError):
        c = {}
    for k in ("startup", "demand", "secondary", "pending", "known"):
        c.setdefault(k, [])
    return c


def classify_new(items, c):
    known = set(c["known"])
    new = [it for it in items if it["id"] not in known]
    if not new:
        return []
    report = []
    if not known:  # first run: what is installed now is already classified
        c["known"] = sorted(it["id"] for it in items)
        new = []
    for it in new:
        if DEMAND_RX.search(it["desc"]):
            c["demand"].append(short(it["id"]))
            report.append(f"{it['id']}=demande")
        elif START_RX.search(it["desc"]):
            c["pending"].append(it["id"])
            report.append(f"{it['id']}=A TRANCHER (demarrage ou secondaire ?)")
        else:
            report.append(f"{it['id']}=secondaire")
        c["known"].append(it["id"])
    c["known"].sort()
    with open(CLASSES, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=1)
    return report


def build(sig):
    items = scan()
    c = load_classes()
    report = classify_new(items, c)
    excluded = set(c["demand"]) | {short(s.split(" (")[0]) for s in c["startup"]}
    excluded.add("autolist-skills-agents-claude-DC")
    docs = []
    for it in items:
        if short(it["id"]) in excluded:
            continue
        name = words(short(it["id"]).replace("-", " ").replace("_", " "))
        docs.append({"id": it["id"], "k": it["kind"][0], "n": name, "d": sorted(set(words(it["desc"])))})
    df = {}
    for d in docs:
        for w in set(d["n"]) | set(d["d"]):
            df[w] = df.get(w, 0) + 1
    idf = {w: round(math.log(len(docs) / n), 2) for w, n in df.items()}
    idx = {"sig": signature(), "docs": docs, "idf": idf, "news": report,
           "startup": c["startup"], "pending": c["pending"]}
    os.makedirs(CACHE, exist_ok=True)
    with open(INDEX, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, separators=(",", ":"))
    return idx


def load():
    sig = signature()
    try:
        with open(INDEX, encoding="utf-8") as f:
            idx = json.load(f)
        if idx.get("sig") == sig:
            idx["news"] = []
            return idx
    except (OSError, ValueError):
        pass
    return build(sig)


def route(prompt, idx):
    q = set()
    for w in words(prompt):
        q.add(w)
        en = FR.get(w)
        if en:
            q.add(en)
    if not q:
        return []
    idf = idx["idf"]
    scored = []
    for d in idx["docs"]:
        s = sum(3 * idf.get(w, 0) for w in q if w in d["n"])
        s += sum(idf.get(w, 0) for w in q if w in d["d"])
        if s >= MIN_SCORE:
            scored.append((s, d["k"], d["id"]))
    scored.sort(reverse=True)
    return scored[:TOP]


def main():
    try:
        payload = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace") or "{}")
    except ValueError:
        payload = {}
    prompt = payload.get("prompt", "")
    if len(prompt.strip()) < 8 or prompt.lstrip().startswith("/"):
        return
    idx = load()
    lines = ["autolist: demarrage = " + " > ".join(idx["startup"])]
    hits = route(prompt, idx)
    if hits:
        tag = {"s": "skill", "a": "agent", "c": "cmd"}
        lines.append("autolist: candidats = " + ", ".join(f"{i} ({tag[k]})" for _, k, i in hits)
                     + ". Si la demande est une tache, invoque le plus pertinent (Skill ou Agent) sans attendre de /commande.")
    lines.append("autolist: skills de demande = jamais auto, seulement si l'utilisateur les nomme.")
    if idx.get("news"):
        lines.append("autolist: nouveaux installes -> " + "; ".join(idx["news"][:8]))
    if idx.get("pending"):
        lines.append("autolist: a trancher avec l'utilisateur -> " + ", ".join(idx["pending"][:5]))
    sys.stdout.buffer.write(("\n".join(lines) + "\n").encode("utf-8"))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # never block the prompt
        sys.stdout.buffer.write(f"autolist: erreur ignoree ({type(e).__name__})\n".encode("utf-8"))
