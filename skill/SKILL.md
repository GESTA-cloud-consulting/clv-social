---
name: clv-social-post
description: Create and publish Chianti Luxury Villas (CLV) social posts end to end — apply the white CLV logo to uploaded photos, propose an on-image claim, write English captions and hashtags adapted to Instagram, Facebook, LinkedIn and Pinterest, show a preview, then publish now, schedule or save as a draft via OnlySocial. Use whenever GESTA shares a brief and/or property photos for CLV social media, or mentions a CLV post, Chianti Luxury Villas content, OnlySocial publishing for CLV, or scheduling villa/castle posts, even if they don't name every step.
---

# CLV social post

Turns a brief and one or more photos into a ready-to-publish post for the four Chianti Luxury Villas channels, using the brand logo, brand fonts and OnlySocial.

**Language:** the whole process — questions, preview labels, explanations, confirmations, error messages — is in **Italian**, concise and professional. Only the post content is in **English**: claim, captions, Pinterest title/description and hashtags. Never switch the conversation to English, even though the copy is English.

## Fixed configuration

| Item | Value |
|---|---|
| OnlySocial workspace | `GESTA` — uuid `0b11d5c3-9762-4418-ab0a-e04c34970418` |
| Instagram | id `68790` (chianti.luxury.villas) |
| Facebook page | id `68791` (Chianti.Luxury.Villas) |
| LinkedIn page | id `68792` (chianti-luxury-villas) |
| Pinterest | id `68789` (chiantiluxuryvillas) |
| Asset repo (public) | `GESTA-cloud-consulting/clv-social` |
| Default link | `https://chiantiluxuryvillas.com/` |
| Timezone | `Europe/Rome` |

The GESTA workspace also contains accounts of other brands (The Coherent System, Coltellerie Italiane). **Only ever use the four CLV ids above.** If one of them is missing or unauthorized in `list-accounts`, stop and tell the user rather than substituting another account.

Pinterest boards (account `chiantiluxuryvillas`) — propose the best fit in the preview, the user confirms:

| Board | Board id | Use for |
|---|---|---|
| Tuscan Castles | `1069253205220283656` | castles, towers, fortified estates, chapels of a castle |
| Tuscan Farmhouse | `1069253205219673735` | farmhouses / casali / poderi, mainly exteriors |
| Tuscan Architecture | `1069253205219723789` | architectural details: arches, stonework, beams, porticoes, verandas, restoration |
| Tuscany Living | `1069253205219678762` | interiors, bedrooms, pools, dining, lifestyle in the property |
| Chianti Living | `1069253205219673748` | Chianti way of life: wine, food, villages, experiences |
| Tuscany's Chianti Countryside | `1069253205219673713` | landscapes, views, vineyards, hills |

If the user mentions a new board, its id can be read from Pinterest (logged-in browser) via `/resource/BoardsResource/get/` for username `chiantiluxuryvillas`.

Brand palette (for claims): white `#FFFFFF` (default), Verde colline `#5c932d`, Terra di Siena `#b64a14`, Terra di Siena Bruciata `#6B3D3D`, Giallo `#fcd870`. Fonts: Cinzel (claims, default), Crimson Pro.

## Workflow

### 1. Gather inputs
You need: the brief, at least one photo, and the link. Ask in one short message only for what is missing. Always state the link that will be used and let the user change it — the default is `https://chiantiluxuryvillas.com/`, but for a specific property the user may give a product page URL.

### 2. Set up the asset repo
The logo, fonts and image script live in the repo, not in this skill.

```bash
test -d /home/claude/clv-social/.git || git clone --depth 1 https://github.com/GESTA-cloud-consulting/clv-social /home/claude/clv-social
git -C /home/claude/clv-social pull -q
```
If cloning or pushing is refused, attach the repo with the `add_repo` tool (owner `GESTA-cloud-consulting`, repo `clv-social`, access `push`) and retry. If pushes are still refused, the Claude GitHub App needs to be installed on the repo — tell the user and stop at the preview.

### 3. Write the copy (English)
Propose, from the brief:

- **Claim** for the image: 2–4 words, Title Case, evocative, e.g. "Comfortable Interior Design", "Wrapped in Nature", "Inside and Out". Optional — skip it if the photo is busy or the user says no claim.
- **Main caption** in the house style:
  1. a hook line (a question or a strong statement), e.g. "What must it be like to live in a tower?"
  2. 1–2 short paragraphs telling the property: place, atmosphere, history, possibilities (residence, investment, hospitality)
  3. a closing line with punch, plus 1–2 fitting emoji (✨🏰👑🌿🍃🍷)
  4. a soft call to action when it fits ("Contact us for more information.")
  Tone: refined, warm, aspirational, never ostentatious; "discreet luxury". No prices or facts not in the brief. Stay faithful to what the photo actually shows: if the brief says "portico" but the photo shows a glazed veranda, word it so both are true and mention the choice in the preview.
- **Hashtags**: pick from the house set and add topical ones from the brief. House set: #Chianti #Tuscany #Italy #TuscanFarmhouse #ChiantiLiving #DreamHome #LuxuryRealEstate #CountrysideEscape #CLV #ChiantiLuxuryVillas. **#CLV and #ChiantiLuxuryVillas are always present, last.**

Then adapt per channel:

| Channel | Adaptation |
|---|---|
| Instagram | Full caption. Links are not clickable: end the CTA with "Discover more, link in bio." instead of a URL. **Max 5 hashtags** (Instagram's limit): #CLV, #ChiantiLuxuryVillas + the 3 most relevant. |
| Facebook | Full caption + the link on its own line before the hashtags. 5–8 hashtags. |
| LinkedIn | More business framing (well-being, investment, value, hospitality potential, rarity) while keeping the story. "Learn more: <link>" before hashtags. 3–5 hashtags. |
| Pinterest | Pinterest is a search engine, so rewrite rather than truncate. Pin **title** ≤ 100 chars, descriptive and keyword-rich (e.g. "Stone Farmhouse in Tuscany with Veranda – Living Inside and Out in Every Season"). Description ≤ 500 chars total: hook + one compact paragraph with searchable words (Tuscany, Chianti, villa, castle, interior design…) + 3–5 hashtags ending with #CLV #ChiantiLuxuryVillas. No emoji, no "link in bio". The link goes in the pin's link field. Propose the board (table above). |

Count characters for Pinterest (show the counts in the preview) and keep Instagram under 2,200.

### 4. Compose the image
For each photo:
```bash
cd /home/claude/clv-social
python3 scripts/compose_image.py <input> <scratchpad>/<YYYY-MM-DD>-<slug>[-n].jpg \
  --claim "<Claim>" [--claim-color white|verde|siena|siena-bruciata|giallo] \
  [--claim-font cinzel|crimson] [--claim-position top|center] [--max-lines 1|2|3] [--focus 0.5] \
  --safe-preview <scratchpad>/<slug>-grid.jpg
```
- Quality is the priority: the script never upscales (a smaller photo keeps its native side), converts to sRGB, and saves a high-quality JPEG (q92, 4:4:4, progressive) without EXIF/GPS. Report any `warnings` from its output to the user in Italian (e.g. photo under 1080px) before going on. Never recompress the output a second time.
- Output is a square (2160×2160, or the photo's short side if smaller); the white logo is placed centred at the bottom automatically (16% of width, 5.5% bottom margin, no effects).
- The claim is auto-fitted inside the central 68% of the width, so it is never cut in Instagram's 3:4 profile grid. Put the claim only on the first image of a carousel.
- `--focus` moves the square crop (0 = top/left, 1 = bottom/right) when the photo isn't square — use it if the subject would be cut.
- Look at the result (Read the image) before showing it: the claim must be legible and must **not cover the subject** (the house, the main feature). If it does, recompose with `--max-lines 1` (one smaller line in the top band) or `--max-lines 2`; if white is not legible, try another palette colour. Also check the logo's contrast on its background. Mention in the preview which variant you chose and why.

Needs Pillow (`pip install pillow --break-system-packages` if missing).

### 5. Preview and decision
Send the composed image(s) and the grid preview with `SendUserFile`, then show the copy as:

```
CLAIM: …
LINK: …

INSTAGRAM
…
FACEBOOK
…
LINKEDIN
…
PINTEREST — board: … — titolo: …
…
```
(Labels and comments in Italian, post text in English, each text in a code block so it's easy to copy.)
Ask the user to choose: **pubblica subito**, **pianifica** (date and time, Europe/Rome) or **salva in bozza**, and to request any change. Apply edits and re-preview until approved. Never publish or schedule without this explicit choice. If the date or time is incomplete or ambiguous (e.g. "il 17" with no month or hour), ask before scheduling; a scheduled time must be in the future.

### 6. Publish via OnlySocial
1. Only after the user's choice, copy the approved image(s) from the scratchpad into `media/` and push: `git add media && git commit -m "Post <slug>" && git push`. Images stay out of the public repo until then. The public URL is
   `https://raw.githubusercontent.com/GESTA-cloud-consulting/clv-social/main/media/<file>` — check it returns 200 with `curl -sI` before continuing.
2. `upload-media-by-url` for each image (workspace uuid above, alt_text = short description). For large files, poll `get-media-upload-status` with the `download_id`. Keep the numeric media `id`s.
3. `create-post` with `account_ids: [68790, 68791, 68792, 68789]`, `timezone: "Europe/Rome"` and `versions`:
   - `account_id: 0` → Facebook caption + media ids, with `options`:
     `{"instagram": {"type": "post"}, "facebook_page": {"type": "post"}, "linkedin_page": {"visibility": "PUBLIC"}, "pinterest": {"title": "<pin title>", "link": "<link>", "boards": {"account-68789": "<board id>"}}}`
   - `account_id: 68790` → Instagram caption + media ids
   - `account_id: 68792` → LinkedIn caption + media ids
   - `account_id: 68789` → Pinterest description + media ids
   - **Put the same full `options` object in every version**, not only in version 0: an account-specific version does not inherit the options of the default one. Without `options.pinterest` (title, link, board) in the Pinterest version, the pin silently fails to publish (no error, no URL).
   - `schedule`: `"now"` for pubblica subito, `"scheduled"` + `scheduled_at: "Y-m-d H:i"` for pianifica, `"draft"` for bozza.
4. Confirm with `get-post`: report status, scheduled time, and — once published — the live URLs per channel. Publishing takes 1–2 minutes after the scheduled time, so a "scheduled" status with no URLs right after "now" is normal: check again before concluding. A post marked `published` where one account has **no `external_url` and no errors** has silently failed on that channel — usually missing options in that account's version. Fix it by creating a new post for that account only, with the options in its version, and tell the user.
5. For **pianifica**, offer to check the outcome shortly after the scheduled time (with `send_later`, if available) and report the links or errors.

The OnlySocial tools come from the OnlySocial connector (load them via ToolSearch "onlysocial" if deferred). If the connector is missing, ask the user to add it in claude.ai Settings → Connectors as a custom connector with URL `https://app.onlysocial.io/os/mcp`.

### 7. Wrap up
One short message in Italian: what was published/scheduled/saved, when, and the links. No recap of steps.

## Notes
- Captions are plain text (no markdown). Line breaks between paragraphs; hashtags on the last line. OnlySocial's summaries show the text without line breaks, but the line breaks are kept on the social networks.
- If the user sends photos without a brief, write from what the photo shows, keep it generic, and say so.
- Test posts: prefix the body with "[TEST]" and save as draft; move them to the trash afterwards with `delete-post`.
