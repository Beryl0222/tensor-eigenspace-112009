"""检查本地交换资料的案例是否互相关联。"""
import unittest

from inspect_fixture import read_session


class MaterialTests(unittest.TestCase):
    def test_linked_records(self):
        d = read_session()
        cap, room, display = d["requests"]
        self.assertEqual(cap["matrix"], room["matrix"])
        self.assertLess(cap["cap"], room["cap"])
        self.assertLess(abs(room["matrix"][1][1]-room["matrix"][2][2]), d["cluster_atol"])
        self.assertGreater(room["matrix"][-1][-1], room["matrix"][0][0])
        gap = display["matrix"][1][1] - display["matrix"][2][2]
        self.assertLess(d["cluster_atol"], gap)
        self.assertLess(gap, d["grad_gap"])
        self.assertGreater(d["profile"]["n"]**2*8, d["profile"]["scratch_bytes"])

    def test_block_source(self):
        from block_fixture import SymmetricBlocks

        profile = read_session()["profile"]
        source = SymmetricBlocks(profile)
        cross = source.read(1, 4, 2, 5)
        self.assertTrue((cross == source.read(2, 5, 1, 4).T).all())
        self.assertEqual(source.read(6, 8, 6, 8).diagonal().tolist(), [4, 2])
        with self.assertRaises(ValueError):
            source.read(0, profile["block_size"] + 1, 0, 1)
