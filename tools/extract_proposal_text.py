#!/usr/bin/env python3
"""Extract human-readable text from a small ReportLab-generated PDF.

Why this exists:
- The proposal is a PDF (binary). We need its exact requirements to implement
  the "trained AI model" and reporting inside AnyLogic without guessing.
- Uses ONLY Python standard library (no venv / no extra installs).

Outputs:
- tools/proposal_extracted.txt

Notes:
- This is a best-effort extractor geared toward ReportLab PDFs that typically
  store page content in FlateDecode streams (often wrapped in ASCII85).
"""

from __future__ import annotations

import argparse
import base64
import re
import zlib
from pathlib import Path


def _parse_filters(dict_bytes: bytes) -> list[str]:
    # Very small parser: handles `/Filter /FlateDecode` and
    # `/Filter [ /ASCII85Decode /FlateDecode ]`.
    m = re.search(rb"/Filter\s+(\[[^\]]+\]|/\w+)", dict_bytes)
    if not m:
        return []

    raw = m.group(1).strip()
    if raw.startswith(b"["):
        names = re.findall(rb"/(\w+)", raw)
        return [n.decode("ascii", "ignore") for n in names]

    if raw.startswith(b"/"):
        return [raw[1:].decode("ascii", "ignore")]

    return []


def _decode_stream(stream_bytes: bytes, filters: list[str]) -> bytes:
    data = stream_bytes.strip()

    # Apply filters in the listed order.
    for f in filters:
        if f == "ASCII85Decode":
            # ReportLab uses Adobe-style ASCII85 with ~> terminator.
            data = base64.a85decode(data, adobe=True)
        elif f == "FlateDecode":
            data = zlib.decompress(data)
        else:
            # Unknown filter; return as-is.
            return data

    return data


def _extract_pdf_literal_strings(payload: bytes) -> list[str]:
    # Extracts PDF literal strings: ( ... ) with escapes.
    out: list[str] = []
    i = 0
    n = len(payload)

    while i < n:
        c = payload[i]
        if c != 0x28:  # '('
            i += 1
            continue

        i += 1
        depth = 1
        buf = bytearray()

        while i < n and depth > 0:
            c = payload[i]

            if c == 0x5C:  # '\\'
                i += 1
                if i >= n:
                    break
                esc = payload[i]

                if esc in b"nrtbf":
                    buf.append({
                        ord("n"): 0x0A,
                        ord("r"): 0x0D,
                        ord("t"): 0x09,
                        ord("b"): 0x08,
                        ord("f"): 0x0C,
                    }[esc])
                elif esc in (0x28, 0x29, 0x5C):  # (, ), \
                    buf.append(esc)
                elif 0x30 <= esc <= 0x37:  # octal up to 3 digits
                    oct_digits = bytes([esc])
                    j = 0
                    while j < 2 and i + 1 < n and 0x30 <= payload[i + 1] <= 0x37:
                        i += 1
                        oct_digits += bytes([payload[i]])
                        j += 1
                    buf.append(int(oct_digits, 8) & 0xFF)
                else:
                    # Treat as literal char.
                    buf.append(esc)

                i += 1
                continue

            if c == 0x28:  # '('
                depth += 1
                buf.append(c)
                i += 1
                continue

            if c == 0x29:  # ')'
                depth -= 1
                if depth == 0:
                    i += 1
                    break
                buf.append(c)
                i += 1
                continue

            buf.append(c)
            i += 1

        try:
            s = buf.decode("latin-1")
        except Exception:
            continue

        if s:
            out.append(s)

    return out


def extract_text(pdf_path: Path) -> str:
    data = pdf_path.read_bytes()

    # Finds: << ... >> stream ... endstream
    # This is sufficient for small ReportLab PDFs.
    # Note: ReportLab commonly uses ASCII85 streams that end with `~>endstream`
    # (no newline before endstream), so the newline before `endstream` must be optional.
    pattern = re.compile(rb"<<(.*?)>>\s*stream\r?\n(.*?)\r?\n?endstream", re.S)

    all_strings: list[str] = []
    for m in pattern.finditer(data):
        dict_bytes = m.group(1)
        stream_bytes = m.group(2)
        filters = _parse_filters(dict_bytes)

        try:
            decoded = _decode_stream(stream_bytes, filters)
        except Exception:
            continue

        strings = _extract_pdf_literal_strings(decoded)
        if strings:
            all_strings.extend(strings)

    # Clean + keep likely-human strings.
    cleaned: list[str] = []
    for s in all_strings:
        s2 = " ".join(s.split())
        if len(s2) < 2:
            continue
        # Must contain letters to be considered useful.
        if not re.search(r"[A-Za-z]", s2):
            continue
        cleaned.append(s2)

    # De-duplicate while preserving order.
    seen: set[str] = set()
    unique: list[str] = []
    for s in cleaned:
        if s in seen:
            continue
        seen.add(s)
        unique.append(s)

    return "\n".join(unique).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract readable text from a ReportLab PDF")
    parser.add_argument(
        "pdf",
        nargs="?",
        default=str(Path(__file__).resolve().parents[1] / "IoT_Simulation_Enhanced_proposal.pdf"),
        help="Path to proposal PDF (default: repo root IoT_Simulation_Enhanced_proposal.pdf)",
    )
    parser.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parent / "proposal_extracted.txt"),
        help="Output text path (default: tools/proposal_extracted.txt)",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    out_path = Path(args.out).resolve()

    text = extract_text(pdf_path)
    out_path.write_text(text, encoding="utf-8")

    print(f"Wrote: {out_path}")
    print(f"Chars: {len(text)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
