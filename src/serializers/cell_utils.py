"""Shared helpers for CSV cell normalization."""


def normalize_cell(cell: str) -> str:
    """Normalize one cell to satisfy CSV contract for empty values."""
    return " " if cell == "" else cell
