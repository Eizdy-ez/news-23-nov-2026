// Entry for make.fun news-image-20261123 (Node 22, standard library only).
//
// "Sum up 23 November's world news in one image": the front page is drawn
// by draw.py (a local build tool, run on the author's machine with Pillow)
// and shipped in this repository as entry.png. This program copies that
// file to the grader's output directory. It uses no network, reads nothing
// but the repository's own entry.png, and writes the same bytes on every
// run, because a byte-for-byte copy cannot vary between runs.
//
// The image sums up Monday 23 November 2026: Jensen Huang's return as
// Nvidia chief executive (+31% shares, Nasdaq +6%); Ukraine sinking the
// Russian corvette Merkury off Benghazi, Libya; COP31 collapsing with no
// deal in Antalya; Russian strikes near Kyiv; drone strikes in Khartoum;
// a factory fire in Indonesia; new US sanctions on Iran; CrowdStrike's
// $43.9bn purchase of Zscaler; West Bank settler violence; and sixteen
// more stories, with a world map of where it happened.
//
// Run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// The grader runs this program twice; both runs must write identical bytes.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The PNG signature every valid PNG file starts with.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
// The competition's limits: at most 1 MiB and 1024 by 1024 pixels.
const MAX_BYTES = 1024 * 1024;
const MAX_DIMENSION = 1024;

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const destination = join(outputDir, "entry.png");

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

// Read the shipped image and check it before anything is written, so a
// broken repository fails loudly instead of producing a bad entry.
const bytes = readFileSync(source);
if (bytes.length > MAX_BYTES) {
  fail(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
  fail("entry.png does not start with the PNG signature");
}
// The IHDR chunk holds the dimensions: bytes 16-19 are the width and
// bytes 20-23 are the height, both big-endian, right after the 8-byte
// signature and the 8-byte chunk header.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
  fail(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, destination);

// Verify the copy: same size, same bytes, same sha256 as the source.
const written = statSync(destination).size;
if (written !== bytes.length) {
  fail(`wrote ${written} bytes, expected ${bytes.length}`);
}
const digest = createHash("sha256").update(bytes).digest("hex");
const check = readFileSync(destination);
if (!check.equals(bytes)) {
  fail("the copied file differs from entry.png");
}
console.log(`wrote ${destination} (${width}x${height}, ${written} bytes)`);
console.log(`sha256 ${digest}`);
