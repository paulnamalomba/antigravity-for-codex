---
name: antigravity-media
description: Analyze an audio, video, or image file with the Antigravity media wrapper, and verify important details.
---

# Antigravity media

Identify the file and user's question before sending it to the external service. Resolve `PLUGIN_ROOT` from this installed skill's absolute `SKILL.md` path: three directories above its directory. Run `"$PLUGIN_ROOT/bin/agy-media" --require-scoped <file> [focus] [--convert] [--tier pro|flash|flash-lo] [--timeout 20m] [--out <path>]`; consult `--help` for details. The `--require-scoped` flag refuses the wrapper’s broad `--yolo` fallback when scoped permissions are unavailable; never remove it silently. The media directory is also the agy workspace and may be readable or writable under the account’s effective permissions; use an isolated directory containing only the intended media and permitted output. This mode is not a machine sandbox. Choose an output path that may be created or overwritten, and note that `--convert` writes a converted file beside the source. Default tier is pro. Allow more time for long recordings. Exit 5 means unsupported format; `--convert` invokes an available conversion tool. Exit 12 indicates timeout; consider shorter segments.

The wrapper outputs a digest and writes the full transcript to a file. Confirm that file exists and inspect relevant timestamped slices for important names, numbers and quotations; these remain uncertain unless verified against the original media. Answer the question with timestamps where available and report the transcript path and verification limits.
