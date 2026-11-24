[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Eizdy-ez/news-23-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Eizdy-ez/news-23-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# Monday 23 November 2026 in One Image

Sum up the world's news of Monday 23 November 2026 in one image — a program that writes the image to `/output/entry.png`. Entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261123).

## The image

An original editorial front page (1024 × 1024 PNG, drawn programmatically with Pillow — no photographs, no copied artwork) that a viewer with no news feed can read. Tiered like a real front page: the three biggest stories get pictures, the next six get cards, and sixteen more run as a text-only list — 25 stories in all — plus a world map with numbered pins:

- **Heroes — Jensen Huang reinstated as Nvidia chief executive, shares up 31% (Nasdaq +6%, S&P 500 +5%); Ukraine sinks the Russian corvette Merkury off Benghazi, Libya, and hits the cargo ship Angara; COP31 collapses with no deal in Antalya after record-long talks.**
- **Cards — Russian strikes kill at least 15 near Kyiv (and a suspected Russian drone spends 8 minutes in Polish airspace); drone strikes hit homes and a UN building in Khartoum; a factory fire in Indonesia kills at least 24 with about 30 missing; Trump imposes sweeping Iran sanctions as Vance meets Qatar's prime minister; CrowdStrike buys Zscaler for $43.9 billion; West Bank settler attacks called "Jewish terrorism" by opposition leader Eisenkot.**
- **Also on Monday:** a world map with numbered pins, and sixteen more stories — the NHS AI breast-cancer screening trial; measles deaths in Pennsylvania rising to nine; Trump pausing the Army's toxic blast in Iowa; the US admitting it deported an American citizen to Mexico; Mexican soldiers attacked after a drug lord's arrest; Gaza strikes killing three on Monday; the Thailand–Cambodia truce holding; Tyson Fury's schizophrenia diagnosis; Malaysia sending Myanmar migrants home; broken trade routes threatening food aid for 7.3 million people; South Korea's education minister resigning over AI cheating; Bolsonaro in intensive care; Democrats taking 258 House seats, their biggest majority since 1992; NATO meeting after Russian missiles land in Poland; Lebanese villagers returning home; and a Pakistan pilot bound for China's Tiangong station.

## How it works

- `draw.py` — draws `entry.png` from scratch with Pillow (run it again to regenerate the image). It is a local build tool only; the grader never runs it.
- `main.ts` — Node 22, standard library only. It copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), after checking the PNG signature, the 1024×1024 size limit and the 1 MiB limit, and it verifies the copy byte for byte. No network access.
- `entry.png` — the 1024 × 1024 image itself.
- `SOURCES.md` — every story with the outlet that reported it on 23 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Two runs write byte-identical files (verified: same sha256).

## License

MIT — see [LICENSE](LICENSE).
