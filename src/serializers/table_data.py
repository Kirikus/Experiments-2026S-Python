"""Tabular data model for CSV import/export round-trip."""

from dataclasses import dataclass, field


def _normalize_cell(cell: str) -> str:
    """
    Normalize one table cell according to task requirements.

    Empty cell values are represented as a single space in CSV.
    """
    if cell == "":
        return " "
    return cell


@dataclass(slots=True)
class TableData:
    """Universal table representation for engineering calculation steps."""

    headers: list[str]
    rows: list[list[str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate and normalize table content right after initialization."""
        self._validate_headers()
        self._normalize_and_validate_rows()

    @property
    def column_count(self) -> int:
        """Return number of columns in the table."""
        return len(self.headers)

    @property
    def row_count(self) -> int:
        """Return number of data rows in the table."""
        return len(self.rows)

    def _validate_headers(self) -> None:
        """Ensure table has at least one non-empty header name."""
        if not self.headers:
            raise ValueError("Table must have at least one header column")

        if any(header == "" for header in self.headers):
            raise ValueError("Header names must not be empty")

    def _normalize_and_validate_rows(self) -> None:
        """Normalize row cells and validate row width against headers."""
        normalized_rows: list[list[str]] = []

        for row in self.rows:
            if len(row) != self.column_count:
                raise ValueError(
                    "Row width does not match headers count: "
                    f"expected {self.column_count}, got {len(row)}"
                )

            normalized_rows.append([_normalize_cell(cell) for cell in row])

        self.rows = normalized_rows

    def add_row(self, row: list[str]) -> None:
        """Add one row to the table with width validation and normalization."""
        if len(row) != self.column_count:
            raise ValueError(
                "Row width does not match headers count: "
                f"expected {self.column_count}, got {len(row)}"
            )

        self.rows.append([_normalize_cell(cell) for cell in row])
