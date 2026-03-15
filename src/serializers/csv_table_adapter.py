"""CSV adapter for universal table import/export."""

import csv
from pathlib import Path

from .table_data import TableData


def _normalize_cell(cell: str) -> str:
    """Normalize one cell to satisfy the required CSV format contract."""
    if cell == "":
        return " "
    return cell


class CSVTableAdapter:
    """Import/export adapter for step-based engineering tables in CSV format."""

    @staticmethod
    def load(filepath: Path) -> TableData:
        """Load CSV file into TableData with header validation and row normalization."""
        with open(filepath, "r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            all_rows = list(reader)

        if not all_rows:
            raise ValueError("CSV file is empty")

        headers = all_rows[0]
        if not headers:
            raise ValueError("CSV header row is empty")

        normalized_rows: list[list[str]] = []
        header_len = len(headers)

        for row in all_rows[1:]:
            if len(row) > header_len:
                raise ValueError(
                    "Row width exceeds header width: "
                    f"expected {header_len}, got {len(row)}"
                )

            if len(row) < header_len:
                row = row + [" "] * (header_len - len(row))

            normalized_rows.append([_normalize_cell(cell) for cell in row])

        return TableData(headers=headers, rows=normalized_rows)

    @staticmethod
    def save(table: TableData, filepath: Path) -> None:
        """Save TableData to CSV keeping required empty-cell representation."""
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(table.headers)

            for row in table.rows:
                writer.writerow([_normalize_cell(cell) for cell in row])
