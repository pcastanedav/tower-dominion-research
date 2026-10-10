import random
import unittest
from mc_doctrines import MCDocState, acquire_with_drafts
from mc_state import MCState
from reinforcement_model import sample_doctrines


class DoctrineDraftRemovalTests(unittest.TestCase):
    def test_ordinary_acquisition_removes_from_future_drafts(self):
        state = MCDocState()
        mc = MCState()
        self.assertIn('D2_14', dict(state.pool(20)))
        acquire_with_drafts(state, 'D2_14', mc, random.Random(1), 20)
        self.assertNotIn('D2_14', dict(state.pool(20)))
        self.assertNotIn('D2_14', sample_doctrines(random.Random(2), state.pool(20), 10000))

    def test_tb_acquisition_advances_branch_and_removes_owned_node(self):
        state = MCDocState(placed_families={0})
        mc = MCState()
        self.assertIn('TB0D1', dict(state.pool(20)))
        acquire_with_drafts(state, 'TB0D1', mc, random.Random(1), 20)
        self.assertIn('TB0D1', state.tb_owned)
        self.assertNotIn('TB0D1', dict(state.pool(20)))
        self.assertIn('TB0D2', dict(state.pool(20)))

    def test_nested_draft_does_not_reoffer_parent(self):
        state = MCDocState()
        mc = MCState()
        acquire_with_drafts(state, 'D2_40', mc, random.Random(4), 20)
        self.assertNotIn('D2_40', dict(state.pool(20)))
        self.assertTrue(state.draft_events)
        for _, offered, _ in state.draft_events:
            self.assertNotIn('D2_40', offered)


if __name__ == '__main__':
    unittest.main()
