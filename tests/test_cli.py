"""Tests for fraq.cli."""

import json
import pytest
from fraq.cli import main
from io import StringIO
import sys


class TestCli:
    def test_explore_json(self, capsys):
        main(["explore", "--depth", "2", "--dims", "2"])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert "value" in data
        assert data["depth"] == 2

    def test_stream_count(self, capsys):
        main(["stream", "--count", "5", "--dims", "2"])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert isinstance(data, list)
        assert len(data) == 5

    def test_schema_fields(self, capsys):
        main(["schema", "--fields", "x:float,y:int,z:str", "--depth", "1", "--branching", "3", "--dims", "3"])
        out = capsys.readouterr().out
        data = json.loads(out)
        assert isinstance(data, list)
        assert len(data) == 3
        assert "x" in data[0]
        assert "y" in data[0]
        assert "z" in data[0]

    def test_csv_format(self, capsys):
        main(["schema", "-f", "csv", "--fields", "a:float,b:int", "--depth", "1", "--branching", "2", "--dims", "2"])
        out = capsys.readouterr().out
        lines = out.strip().splitlines()
        assert lines[0].strip() == "a,b"
        assert len(lines) == 3  # header + 2

    def test_no_command_exits(self):
        with pytest.raises(SystemExit):
            main([])
