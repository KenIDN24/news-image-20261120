# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/KenIDN24/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/KenIDN24/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

The world in one day: a one-image broadsheet of Friday 20 November 2026's world news. The lead stories are the first Trump–Xi–Putin trilateral summit in Shenzhen and the ICJ's ruling that Myanmar committed genocide against the Rohingya, with Russia's strike on Kyiv, Anthropic's record IPO, the COP31 draft dropping fossil fuels, and briefs from the Middle East, Asia-Pacific, Taiwan, Europe and more — 14 stories with per-story sources in `SOURCES.md`. The picture is drawn by `render.py`, a pure Python standard-library renderer (own PNG encoder, bitmap font and layout, no third-party packages), and `main.py` writes it to the output directory byte-for-byte identical on every run.

## Run it

```sh
python3 main.py
```

Writes `entry.png` (1024×1024 PNG) to `$MAKEFUN_OUTPUT_DIR`, or `/output`, falling back to the repository folder.

---

<sub>Entered on [make.fun](https://make.fun/?ref=c8w480ny&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
