import unittest
from expertise_wave35 import construction_wave, target_doctrine_weights, run, POLICIES

class ExpertiseWave35Tests(unittest.TestCase):
    def test_wave10_floor(self):
        self.assertEqual(construction_wave(2),10)
        self.assertEqual(construction_wave(16),16)
        self.assertIsNone(construction_wave(None))

    def test_amplifier_additive_target_only(self):
        pools=[dict(target_doctrine_weights('Lions',10,'CB14',set(),True,n,other_families=('CB01',))) for n in (0,1,2)]
        self.assertEqual([p['TBCB14D4'] for p in pools],[300,600,900])
        self.assertEqual([p['TBCB01D4'] for p in pools],[300,300,300])

    def test_progression_gating(self):
        p=dict(target_doctrine_weights('Lions',10,'CB14',set(),True))
        self.assertIn('TBCB14D4',p)
        self.assertNotIn('TBCB14D5',p)
        p=dict(target_doctrine_weights('Lions',10,'CB14',{'TBCB14D4'},True))
        self.assertNotIn('TBCB14D4',p)
        self.assertIn('TBCB14D5',p)

    def test_guaranteed_wave10_build(self):
        r=run(7,guaranteed_blueprint=True)
        self.assertEqual(r.construction_wave,10)
        self.assertTrue(all(w>=10 for w in r.expertise_waves.values()))

    def test_d7_or_gate(self):
        prefix='TBCB14D'
        for predecessor in ('3','6'):
            p=dict(target_doctrine_weights('Lions',15,'CB14',{prefix+predecessor},True))
            self.assertIn(prefix+'7',p)
        self.assertNotIn(prefix+'7',dict(target_doctrine_weights('Lions',15,'CB14',set(),True)))

    def test_d7_result_consistency(self):
        for seed in range(1,21):
            r=run(seed,guaranteed_blueprint=True)
            self.assertEqual(r.d7_wave,r.expertise_waves.get(7))
            if r.d7_wave is not None:
                self.assertIn(r.d7_route,('cost','efficiency','both'))

    def test_eleanor_draft_cadence(self):
        self.assertEqual(run(3,eleanor=True).eleanor_drafts,17)
        self.assertEqual(run(3,eleanor=False).eleanor_drafts,0)

    def test_real_family_ids(self):
        r=run(2,guaranteed_blueprint=True)
        self.assertTrue(all(1 <= k <= 7 for k in r.expertise_waves))
        self.assertTrue(all(w >= 10 for w in r.expertise_waves.values()))

    def test_all_policies_deterministic(self):
        for policy in POLICIES:
            a=run(11,eleanor=True,policy=policy)
            self.assertEqual(a,run(11,eleanor=True,policy=policy))
            self.assertGreaterEqual(a.attenuator_offer_count,a.attenuator_acquired)
            self.assertGreaterEqual(a.amplifier_offer_count,a.amplifier_acquired)

if __name__=='__main__': unittest.main()
