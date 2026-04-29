from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List


INSERT_RE = re.compile(
    r"^INSERT INTO MQTT_READY VALUES\((?P<id>\d+),(?P<packet_size>[^,]+),(?P<inter_arrival>[^,]+),(?P<flow_duration>[^,]+),'(?P<ts>[^']+)'\)\s*$"
)


@dataclass(frozen=True)
class MqttReadyRow:
    id: int
    packetSize: float
    interArrival: float
    flowDuration: float
    arrivalTimestamp: str


def _iter_rows(db_script_lines: Iterable[str]) -> Iterable[MqttReadyRow]:
    for raw_line in db_script_lines:
        if not raw_line.startswith("INSERT INTO MQTT_READY VALUES("):
            continue

        line = raw_line.strip()
        match = INSERT_RE.match(line)
        if not match:
            continue

        yield MqttReadyRow(
            id=int(match.group("id")),
            packetSize=float(match.group("packet_size")),
            interArrival=float(match.group("inter_arrival")),
            flowDuration=float(match.group("flow_duration")),
            arrivalTimestamp=match.group("ts"),
        )


def extract_mqtt_ready(db_script_path: Path) -> List[MqttReadyRow]:
    with db_script_path.open("r", encoding="utf-8", errors="replace") as f:
        rows = list(_iter_rows(f))

    rows.sort(key=lambda r: r.id)
    return rows


def write_json(rows: List[MqttReadyRow], out_path: Path, source_rel: str) -> None:
    payload = {
        "generatedAt": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "source": source_rel.replace("\\", "/"),
        "rowCount": len(rows),
        "rows": [r.__dict__ for r in rows],
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_csv(rows: List[MqttReadyRow], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "packetSize",
                "interArrival",
                "flowDuration",
                "arrivalTimestamp",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> int:
    repo_root = _default_repo_root()

    parser = argparse.ArgumentParser(
        description=(
            "Extract MQTT_READY rows from AnyLogic HSQL db.script into JSON/CSV for the dashboard."
        )
    )
    parser.add_argument(
        "--db-script",
        type=Path,
        default=repo_root / "FinalCCNProject" / "database" / "db.script",
        help="Path to AnyLogic db.script (default: FinalCCNProject/database/db.script)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=repo_root / "dashboard" / "data",
        help="Output directory (default: dashboard/data)",
    )

    args = parser.parse_args()

    db_script_path: Path = args.db_script
    out_dir: Path = args.out_dir

    if not db_script_path.exists():
        raise SystemExit(f"db.script not found: {db_script_path}")

    rows = extract_mqtt_ready(db_script_path)

    out_json = out_dir / "mqtt_ready.json"
    out_csv = out_dir / "mqtt_ready.csv"

    # Use repo-relative source path for portability
    try:
        source_rel = str(db_script_path.resolve().relative_to(repo_root.resolve()))
    except Exception:
        source_rel = str(db_script_path)

    write_json(rows, out_json, source_rel=source_rel)
    write_csv(rows, out_csv)

    first_ts = rows[0].arrivalTimestamp if rows else "-"
    last_ts = rows[-1].arrivalTimestamp if rows else "-"

    print(f"Extracted {len(rows)} rows")
    print(f"Time range: {first_ts} → {last_ts}")
    print(f"Wrote: {out_json}")
    print(f"Wrote: {out_csv}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
