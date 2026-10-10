"""Approved Mission Control economic assumptions; independent of combat simulation."""
from dataclasses import dataclass


@dataclass(frozen=True)
class MCEconomy:
    wave: int
    mc_built: int
    battlefronts: int = 4
    extensions_per_mc: float = 2.5

    @property
    def discount_mcs(self):
        return max(0, self.mc_built - 1)

    @property
    def base_reroll_cost(self):
        return 25 if self.wave < 46 else 55  # +30 at Wave 46: provisional

    @property
    def reroll_cost(self):
        return max(5, self.base_reroll_cost - 5 * self.discount_mcs)

    @property
    def reroll_savings(self):
        return self.base_reroll_cost - self.reroll_cost

    @property
    def recon_per_wave(self):
        return 10 if self.mc_built else 0

    @property
    def supply_per_wave(self):
        return 400 if self.mc_built and self.wave <= 55 else 0

    @property
    def global_damage_bonus_percent(self):
        return self.mc_built * self.extensions_per_mc * 4 * self.battlefronts


def economy_history(history, rerolls_per_wave=0):
    """Annotate per-wave snapshots. Recon savings depend on assumed reroll volume."""
    if rerolls_per_wave < 0:
        raise ValueError('rerolls_per_wave must be nonnegative')
    recon_produced = supply_produced = reroll_recon_saved = 0
    rows = []
    for snapshot in history:
        economy = MCEconomy(snapshot['wave'], snapshot['mc_built'])
        recon_produced += economy.recon_per_wave
        supply_produced += economy.supply_per_wave
        reroll_recon_saved += economy.reroll_savings * rerolls_per_wave
        rows.append({**snapshot, 'reroll_cost': economy.reroll_cost,
                     'reroll_recon_saved': reroll_recon_saved,
                     'recon_produced': recon_produced,
                     'supply_produced': supply_produced,
                     'global_damage_bonus_percent': economy.global_damage_bonus_percent})
    return rows
