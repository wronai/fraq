"""Tests for fraq.core — FraqNode, FraqSchema, FraqCursor."""

import pytest
from fraq.core import FraqNode, FraqSchema, FraqCursor, _vec_add, _vec_scale, _vec_hash


# ---------------------------------------------------------------------------
# Vector helpers
# ---------------------------------------------------------------------------

class TestVectorHelpers:
    def test_vec_add(self):
        assert _vec_add((1.0, 2.0), (3.0, 4.0)) == (4.0, 6.0)

    def test_vec_scale(self):
        assert _vec_scale((2.0, 3.0), 0.5) == (1.0, 1.5)

    def test_vec_hash_deterministic(self):
        v = (1.0, 2.0, 3.0)
        assert _vec_hash(v, 42) == _vec_hash(v, 42)

    def test_vec_hash_different_seeds(self):
        v = (1.0, 2.0, 3.0)
        assert _vec_hash(v, 0) != _vec_hash(v, 1)


# ---------------------------------------------------------------------------
# FraqNode
# ---------------------------------------------------------------------------

class TestFraqNode:
    def test_default_value_in_unit_range(self):
        node = FraqNode(position=(0.0, 0.0, 0.0))
        assert 0.0 <= node.value < 1.0

    def test_deterministic_value(self):
        a = FraqNode(position=(1.0, 2.0, 3.0), seed=99)
        b = FraqNode(position=(1.0, 2.0, 3.0), seed=99)
        assert a.value == b.value

    def test_different_position_different_value(self):
        a = FraqNode(position=(0.0, 0.0, 0.0))
        b = FraqNode(position=(1.0, 0.0, 0.0))
        assert a.value != b.value

    def test_zoom_increases_depth(self):
        root = FraqNode(position=(0.0, 0.0, 0.0))
        child = root.zoom(steps=3)
        assert child.depth == 3

    def test_zoom_same_path_same_node(self):
        root = FraqNode(position=(0.0, 0.0, 0.0))
        a = root.zoom((1.0, 0.0, 0.0), steps=2)
        # re-walk: root -> same direction twice
        b = root.zoom((1.0, 0.0, 0.0)).zoom((1.0, 0.0, 0.0))
        assert a.value == b.value
        assert a.depth == b.depth

    def test_children_default_branching(self):
        root = FraqNode(position=(0.0, 0.0))
        kids = root.children(branching=4)
        assert len(kids) == 4
        assert all(isinstance(k, FraqNode) for k in kids)

    def test_children_custom_directions(self):
        root = FraqNode(position=(0.0, 0.0))
        dirs = [(1.0, 0.0), (0.0, 1.0)]
        kids = root.children(directions=dirs)
        assert len(kids) == 2

    def test_custom_generator(self):
        gen = lambda n: n.depth * 10
        root = FraqNode(position=(0.0,), generator=gen)
        child = root.zoom(steps=5)
        assert child.value == 50

    def test_to_dict_no_children(self):
        node = FraqNode(position=(1.0, 2.0), seed=7)
        d = node.to_dict()
        assert "position" in d
        assert d["depth"] == 0
        assert "children" not in d

    def test_to_dict_with_children(self):
        root = FraqNode(position=(0.0, 0.0))
        root.zoom((1.0, 0.0))
        d = root.to_dict(max_depth=1)
        assert "children" in d

    def test_infinite_zoom_no_crash(self):
        """Zoom 100 levels deep — should not blow up."""
        root = FraqNode(position=(0.0, 0.0, 0.0))
        node = root.zoom(steps=100)
        assert node.depth == 100
        assert 0.0 <= node.value < 1.0


# ---------------------------------------------------------------------------
# FraqSchema
# ---------------------------------------------------------------------------

class TestFraqSchema:
    def test_add_field_fluent(self):
        root = FraqNode(position=(0.0, 0.0, 0.0))
        schema = FraqSchema(root=root)
        result = schema.add_field("x").add_field("y")
        assert result is schema
        assert len(schema.fields) == 2

    def test_record_produces_all_fields(self):
        root = FraqNode(position=(0.0, 0.0, 0.0))
        schema = FraqSchema(root=root)
        schema.add_field("a", "float")
        schema.add_field("b", "int")
        schema.add_field("c", "str")
        schema.add_field("d", "bool")
        rec = schema.record()
        assert set(rec.keys()) == {"a", "b", "c", "d"}
        assert isinstance(rec["a"], float)
        assert isinstance(rec["b"], int)
        assert isinstance(rec["c"], str)
        assert isinstance(rec["d"], bool)

    def test_records_generator_yields(self):
        root = FraqNode(position=(0.0, 0.0))
        schema = FraqSchema(root=root)
        schema.add_field("val")
        recs = list(schema.records(depth=1, branching=3))
        assert len(recs) == 3  # depth=1, branching=3 → 3 records
        assert all("val" in r for r in recs)

    def test_records_depth_2(self):
        root = FraqNode(position=(0.0, 0.0))
        schema = FraqSchema(root=root)
        schema.add_field("v")
        recs = list(schema.records(depth=2, branching=2))
        # depth 2, branching 2 → 2*2 = 4 records
        assert len(recs) == 4

    def test_transform_applied(self):
        root = FraqNode(position=(0.0, 0.0), generator=lambda n: 0.5)
        schema = FraqSchema(root=root)
        schema.add_field("x", "float", transform=lambda v: v * 100)
        rec = schema.record()
        assert rec["x"] == 50.0

    def test_bytes_type(self):
        root = FraqNode(position=(0.0,))
        schema = FraqSchema(root=root)
        schema.add_field("raw", "bytes")
        rec = schema.record()
        assert isinstance(rec["raw"], bytes)


# ---------------------------------------------------------------------------
# FraqCursor
# ---------------------------------------------------------------------------

class TestFraqCursor:
    def test_initial_depth_zero(self):
        root = FraqNode(position=(0.0, 0.0))
        cursor = FraqCursor(root=root)
        assert cursor.depth == 0
        assert cursor.current is root

    def test_advance_increases_depth(self):
        root = FraqNode(position=(0.0, 0.0))
        cursor = FraqCursor(root=root)
        cursor.advance()
        assert cursor.depth == 1

    def test_back_decreases_depth(self):
        root = FraqNode(position=(0.0, 0.0))
        cursor = FraqCursor(root=root)
        cursor.advance()
        cursor.advance()
        cursor.back()
        assert cursor.depth == 1

    def test_back_at_root(self):
        root = FraqNode(position=(0.0, 0.0))
        cursor = FraqCursor(root=root)
        cursor.back()  # should not crash
        assert cursor.depth == 0

    def test_reset(self):
        root = FraqNode(position=(0.0, 0.0))
        cursor = FraqCursor(root=root)
        cursor.advance()
        cursor.advance()
        cursor.advance()
        cursor.reset()
        assert cursor.depth == 0

    def test_snapshot_serialisable(self):
        root = FraqNode(position=(0.0, 0.0))
        cursor = FraqCursor(root=root)
        cursor.advance((1.0, 0.0))
        snap = cursor.snapshot()
        assert "path" in snap
        assert len(snap["path"]) == 1

    def test_deterministic_path(self):
        root = FraqNode(position=(0.0, 0.0, 0.0))
        c1 = FraqCursor(root=root)
        c2 = FraqCursor(root=root)
        d = (1.0, 0.0, 0.0)
        c1.advance(d)
        c1.advance(d)
        c2.advance(d)
        c2.advance(d)
        assert c1.current.value == c2.current.value
