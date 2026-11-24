// news-image-20261124 — entrypoint (Node 22, standard library only).
// The image is entry.png beside this file, drawn by render.py from
// stories.json (36 sourced stories of Tuesday 24 November 2026).
// This program copies it to the grader's output directory, so both
// runs write exactly the same bytes. Verified byte-identical in this
// repo: render.py twice and main.ts twice all produce the same sha256.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

copyFileSync(
  new URL("./entry.png", import.meta.url),
  join(process.env.MAKEFUN_OUTPUT_DIR ?? "/output", "entry.png"),
);
