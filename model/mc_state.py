"""Mission Control inventory and special-draft state transitions.

This module models user-approved economic timing assumptions, not verified
in-game construction costs or exact reward candidate sampling.
"""
from collections import deque
from dataclasses import dataclass, field


@dataclass
class MCState:
    wave: int = 1
    mc_in_hand: int = 0
    mc_built: int = 0
    mc_1a_active: int = 0
    mc_3a_processed: int = 0
    amplifier_in_hand: int = 0
    amplifier_built: int = 0
    amplifier_mc_targeted: int = 0
    first_mc_wave: int | None = None
    first_mc_built_wave: int | None = None
    first_amplifier_wave: int | None = None
    placed_building_types: set = field(default_factory=set)
    draft_queue: deque = field(default_factory=deque)
    drafts_resolved: int = 0
    censored: bool = False
    softlock_wave: int | None = None
    mc_build_target: int | None = None
    mc_reserve_target: int = 0
    mc_batch_size: int = 3
    mc_established: bool = False
    mc_selective_this_wave: bool = False
    mc_draft_selective_this_wave: bool = False

    @property
    def mc_owned(self):
        return self.mc_in_hand + self.mc_built

    def acquire(self, building, copies=1, ordinary=False, red=False):
        if copies < 0:
            raise ValueError('copies cannot be negative')
        count = copies * (2 if ordinary and red else 1)
        if building == 'MC':
            self.mc_in_hand += count
            if count and self.first_mc_wave is None:
                self.first_mc_wave = self.wave
        elif building == 'Amplifier':
            self.amplifier_in_hand += count
            if count and self.first_amplifier_wave is None:
                self.first_amplifier_wave = self.wave
        else:
            raise ValueError('unsupported building')

    def build(self, mc_count=None, amplifier_count=None, tier3_wave=40):
        if mc_count is None:
            mc_count = self.mc_in_hand if self.mc_build_target is None else min(self.mc_in_hand, max(0, self.mc_build_target - self.mc_built))
        amplifier_count = self.amplifier_in_hand if amplifier_count is None else amplifier_count
        if not 0 <= mc_count <= self.mc_in_hand:
            raise ValueError('invalid MC build count')
        if not 0 <= amplifier_count <= self.amplifier_in_hand:
            raise ValueError('invalid Amplifier build count')
        self.mc_in_hand -= mc_count
        self.mc_built += mc_count
        self.mc_1a_active += mc_count
        self.amplifier_in_hand -= amplifier_count
        self.amplifier_built += amplifier_count
        if mc_count and self.first_mc_built_wave is None:
            self.first_mc_built_wave = self.wave
        if mc_count:
            self.placed_building_types.add('MC')
        if amplifier_count:
            self.placed_building_types.add('Amplifier')
        self.amplifier_mc_targeted = self.amplifier_built if self.mc_built else 0
        if self.wave >= tier3_wave:
            newly_processed = self.mc_built - self.mc_3a_processed
            self.mc_3a_processed += newly_processed
            self.draft_queue.extend(['MC3A'] * (2 * newly_processed))

    def upgrade_3a(self, count):
        """Spend abstract early-game upgrade opportunities on built, unupgraded MCs."""
        if not 0 <= count <= self.mc_built - self.mc_3a_processed:
            raise ValueError('invalid 3A upgrade count')
        self.mc_3a_processed += count
        self.draft_queue.extend(['MC3A'] * (2 * count))

    def resolve_drafts(self, offer, max_drafts=10000, tier3_wave=40):
        """Resolve queued drafts; offer(state) returns True if MC is selected.

        Limit is a censoring boundary, not a gameplay restriction.
        """
        if max_drafts < 0:
            raise ValueError('max_drafts cannot be negative')
        resolved_here = 0
        while self.draft_queue and resolved_here < max_drafts:
            self.draft_queue.popleft()
            resolved_here += 1
            self.drafts_resolved += 1
            if offer(self):
                self.acquire('MC')
                if self.mc_reserve_target == 0:
                    self.build(amplifier_count=0, tier3_wave=tier3_wave)
        if self.draft_queue:
            self.censored = True
        return resolved_here
