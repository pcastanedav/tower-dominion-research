from dataclasses import dataclass, field
from reinforcement_model import admits_tb_family

@dataclass
class FamilyIntroduction:
    third_tower: str | None = None
    introduced: dict = field(default_factory=dict)

    def advance(self, wave, acquired_towers=(), rng=None):
        if wave >= 2:
            self.introduced.setdefault('Mirador', 0)
        if wave >= 11:
            self.introduced.setdefault('Bunker', 1)
        if wave >= 21 and 2 not in self.introduced.values():
            eligible = sorted(t for t in set(acquired_towers) if admits_tb_family(t) and t not in self.introduced)
            if self.third_tower is not None:
                eligible = [t for t in eligible if t == self.third_tower]
            if eligible:
                selected = rng.choice(eligible) if rng is not None else eligible[0]
                self.introduced[selected] = 2
        return set(self.introduced.values())
