# Obsidian Vault Setup (automated files created)

I added templates, sample notes, a dashboard (Dataview), a Kanban example, an AI draft template, an `assets/images` folder, and a CSS snippet under `.obsidian/snippets/`.

Follow these steps inside Obsidian to complete the setup:

1. Open this folder as your vault in Obsidian.
2. Enable core Templates: Settings → Core Plugins → Templates.
3. Install these community plugins (Settings → Community plugins → Browse):
   - Kanban
   - Dataview
   - Excalidraw (optional)
   - Image Converter (optional)
   - Style Settings (optional)
   - Obsidian Git (optional)

4. Enable the CSS snippet: Settings → Appearance → CSS snippets → enable `folder-colors.css`.
5. Open `Dashboard.md` and install/enable `Dataview` to view queries.
6. Edit the Templates files in `Templates/` to fit your preferred placeholders.

Optional: initialize a Git repo from the vault folder and push to GitHub for versioned backups:

```bash
cd "C:\Users\PCGAME\Desktop\story&universes\chain-weapon-story"
git init
git add .
git commit -m "Initial vault scaffold"
# create a GitHub repo, then:
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

If you'd like, I can also configure an initial Git commit and push for you (you must provide a GitHub repo URL or credentials).
