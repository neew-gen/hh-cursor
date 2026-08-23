# Contract: Portfolio from GitHub (Upwork fill)

Browser fill step for Upwork **Portfolio** in `/upwork-profile-create`.

**Parsing repos is NOT done here.** Run `/project-portfolio-extract` (feature 009) first to produce
`artifacts/project-portfolio-extract/<slug>.yaml`, then fill Upwork from those artifacts.

## Step 0 — Extract portfolio text (feature 009)

If portfolio artifacts are missing:

1. Run `/project-portfolio-extract` with user URLs / ZIP / local paths.
2. Wait for artifacts at `artifacts/project-portfolio-extract/<slug>.yaml`.
3. Each artifact provides: `title`, `description`, `project_url`, `skills`.

Do not shallow-clone or compose descriptions inline in 008 when 009 artifacts exist.

## Project selection (mandatory)

| Step | Action |
|------|--------|
| 1 | Collect candidates from user, profile `portfolio_links`, or existing 009 artifacts |
| 2 | Flag stale projects (`stale` in 009 facts or `last_commit_date` > ~2 years) |
| 3 | `AskQuestion`: which projects to add/update on Upwork |
| 4 | Skip rejected or unapproved stale projects |

Ask what to do with **existing** Upwork portfolio cards (keep / update / replace) before deleting.

## Upwork UI limit: skills (mandatory)

Upwork portfolio modal allows **at most 5 skills** per item (`Skills and deliverables`).

| Rule | Detail |
|------|--------|
| Hard cap | Never type/select more than **5** skills in one portfolio entry |
| 009 artifact may list more | Trim before browser fill; keep `skills` in fill-plan draft ≤ 5 |
| Large / multi-repo project | Pick **1–2 representative skills per sub-area**, then cap at 5 total for the card |
| Prefer breadth over exhaustiveness | One card = one story; do not mirror the full monorepo stack |

### Skill selection (agent)

1. Start from 009 artifact `skills` only — **do not** add tags from 009 `stack` autodetect unless they are already in `skills` (e.g. automation/Python repo must not pick up Vue/TypeScript from unrelated stack noise).
2. If count > 5, keep the skills that best match **title + description** and the user's role on the project.
3. Include **design/UI** only when the user actually owned product/UX (e.g. solo founder).
4. Confirm trimmed list in `tmp/upwork-portfolio-draft.json` before browser fill.

**Example — Castle Keepers** (fullstack solo product, one card):

```yaml
skills: ["TypeScript", "Vue.js", "Node.js", "NestJS", "UI/UX Design"]
```

Do **not** also add PostgreSQL, Redis, Docker, Git on the same card — those are implied by the stack text in `description`.

## Browser fill

Use profile **editor** URL (no `viewMode=1`): `https://www.upwork.com/freelancers/~<id>`.

1. Load fields from `artifacts/project-portfolio-extract/<slug>.yaml` (trim `skills` to ≤ 5 per rules above)
2. Profile page → **Add portfolio** (or edit existing draft)
3. Fill `title`, role (optional), `description`, select **≤ 5** `skills` (slow typeahead → pick `[role=option]`)
4. Optional: **Add a web link** → paste `project_url`
5. **Save as draft** (mandatory — see below); do **not** navigate away until draft is visible under **Drafts**
6. Stop before **Publish**; tell user to add thumbnail (see Thumbnail step)
7. Repeat per approved artifact

### Draft save (mandatory for Portfolio)

Unlike other profile sections (default: wait for user Save), **each portfolio item MUST be saved as draft by the agent** after the form is filled:

| Step | Action |
|------|--------|
| 1 | Click **Save as draft** |
| 2 | Wait until dialog closes and card appears under **Drafts** (not «No drafts yet») |
| 3 | **Do not** reload profile or open another tab until step 2 succeeds |
| 4 | Message user: open the draft and **upload a thumbnail image** (required before Publish) |

If save fails, retry **Save as draft**; do not leave the modal with unsaved data.

### Thumbnail step (user)

Upwork often disables **Publish** until a thumbnail exists (web link alone may not generate one).

After draft save, agent tells the user:

> Черновик «{title}» сохранён во вкладке Drafts. Откройте его и загрузите изображение (thumbnail) — без него Publish недоступен. Когда добавите картинку, напишите — продолжим или опубликуем.

Agent does **not** invent screenshots; user uploads manually.

### Skills typeahead (browser)

- Type slowly into combobox; wait ~2s for options (initial «No results» is normal)
- `ArrowDown` → click exact `[role=option]` match
- Bulk/CDP inject often fails — use `browser_type` + click option per skill

### Upwork skill DB gaps

If typeahead returns no exact match after wait + `ArrowDown`, pick the closest Upwork tag and note the substitution for the user:

| 009 / intended skill | Upwork substitute (when missing) |
|----------------------|----------------------------------|
| Vitest | Unit Testing |
| Vite | Open Source or npm (Vite itself is not in the DB; «Vite» may match unrelated tags) |

Do not force a wrong tag — fewer accurate skills beat invented ones.

### Web link (browser)

1. **Add a web link** opens a **sub-dialog** («Add a web link»).
2. Field: `input[placeholder="Article or website link"]` (not `aria-label`).
3. `browser_fill` alone often leaves **Add** disabled — set value via native setter + `InputEvent('input')` + `change`, then click **Add**.
4. Success: link preview appears in the main portfolio modal before **Save as draft**.

## Optional fill-plan draft

```yaml
portfolio_items:
  - title: "..."
    description: "..."
    project_url: "https://github.com/..."
    skills: ["Vue.js", "TypeScript"]
    artifact_path: artifacts/project-portfolio-extract/vue-use-api-call.yaml
    approved_by_user: true
```

## Constraints

- Facts only from 009 artifacts — no re-invention during browser fill
- **≤ 5 skills** per portfolio item (Upwork UI)
- Thumbnail/screenshot: manual on Upwork (agent does not invent assets)
- Portfolio: agent clicks **Save as draft**; user adds image; Publish only with user consent
