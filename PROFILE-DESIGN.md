# Profile motion design

The profile retains Somyajit's original introduction, learning topics, and goals.

## Edit the visuals

- `assets/profile-header.svg`: midnight blue banner, orbiting cyan/violet particles, traveling line highlight, and code symbol.
- `assets/typing.svg`: six learning topics, typed in a repeating 36-second sequence.
- Both custom assets use embedded CSS, system fonts, and no scripts or external requests. Reduced-motion preferences stop their animations.
- `.github/workflows/snake.yml`: regenerates the contribution snake daily at 01:17 UTC (06:47 IST), on workflow/source changes, and through Run workflow.
- `scripts/publish_snake.py`: publishes only the two generated snake SVGs to the `output` branch. It preserves other files and existing branch history, skips unchanged images, and never force-pushes.
- The workflow uses the repository's automatic `GITHUB_TOKEN`; no personal access token or paid image service is needed.
- Snake generator: https://github.com/Platane/snk (pinned v3 revision). README selects the matching light/dark variant.

## Remove or change animations

Edit the image blocks in `README.md`. Disable the snake workflow in Actions to stop daily updates. Existing assets remain usable.
