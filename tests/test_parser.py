"""Tests for dashboard/parser.py"""
import sys
from pathlib import Path

# Add repo root to path so `dashboard` is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from dashboard.parser import parse_md_table, parse_ranking_table, parse_scorecard, discover_rounds

REPO_ROOT = Path(__file__).parent.parent
