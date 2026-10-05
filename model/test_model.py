import unittest, sys
sys.path.insert(0,'/home/pcastaneda/Documents/tower-dominion-analysis/model')
import reinforcement_model as m
class RewardModelTests(unittest.TestCase):
 def test_outer_weights_sum_100(self): self.assertEqual(sum(w for _,w in m.OUTER),100)
 def test_baseline_layout(self): self.assertEqual(3*2,6)
 def test_doctrine_slot_baseline(self):
  p=.29; self.assertAlmostEqual(1-(1-p)**6,0.871899716079,12); self.assertAlmostEqual(6*p,1.74,12)
 def test_doctrine_tier_unlocks(self):
  self.assertEqual(max(0,-10+2*(6-1)),0); self.assertEqual(max(0,-10+2*(7-1)),2)
  self.assertEqual(max(0,-20+2*(11-1)),0); self.assertEqual(max(0,-20+2*(12-1)),2)
 def test_fresh_family_weight(self):
  self.assertEqual(2*100*3,600); self.assertEqual(2*100*12,2400)
 def test_deployment_ids_present(self):
  p=dict(m.wave_weights('Lions',7)); self.assertEqual(p['ATT_I'],100); self.assertEqual(p['AMP_I'],100); self.assertEqual(p['ATT_II'],2); self.assertEqual(p['AMP_II'],2)
 def test_deployment_ii_absent_before_positive_weight(self): self.assertNotIn('AMP_II',dict(m.wave_weights('Lions',6)))
 def test_faction_wave1_denominators(self):
  self.assertEqual(sum(w for _,w in m.wave_weights('Iron',1)),3900); self.assertEqual(sum(w for _,w in m.wave_weights('Lions',1)),3800); self.assertEqual(sum(w for _,w in m.wave_weights('Pargan',1)),3400)
 def test_denshikova_family_cost(self):
  base=sum(w for _,w in m.wave_weights('Lions',1,0,12)); one=sum(w for _,w in m.wave_weights('Lions',1,1,12)); self.assertEqual(one-base,2400)

class CommanderReinforcementTests(unittest.TestCase):
 def test_standard_and_tander_card_counts(self):
  import random
  standard=m.doctrine_screen(random.Random(1),'Lions',1,card_count=m.COMMANDER_REINFORCEMENT_RULES['standard']['card_count'])
  tander=m.doctrine_screen(random.Random(1),'Lions',1,card_count=m.COMMANDER_REINFORCEMENT_RULES['tander']['card_count'])
  self.assertEqual((len(standard),sum(map(len,standard))),(3,6))
  self.assertEqual((len(tander),sum(map(len,tander))),(4,8))
 def test_magel_cadence(self):
  self.assertEqual([w for w in range(1,9) if m.magel_draft_due(w)],[2,4,6,8])
 def test_magel_draft_is_three_unique_doctrines(self):
  import random
  d=m.magel_doctrine_draft(random.Random(7),'Lions',12,placed_families={0})
  self.assertEqual(len(d),3); self.assertEqual(len(set(d)),3)
 def test_magel_uses_current_progression_state(self):
  import random
  d=m.magel_doctrine_draft(random.Random(1),'Lions',1,tb_owned={'TB0D1'},placed_families={0})
  self.assertNotIn('TB0D1',d)
  pool=dict(m.dynamic_doctrine_pool_fast('Lions',1,tb_owned={'TB0D1'},placed_families={0}))
  self.assertIn('TB0D2',pool); self.assertIn('TB0D4',pool)

class CommanderDynamicRunnerTests(unittest.TestCase):
 def test_magel_special_only_on_even_waves(self):
  r=m.run_commander_dynamic_policy(waves=4,commander='magel',seed=2,policy='none')
  self.assertEqual([bool(x[3]) for x in r['history']],[False,True,False,True])
 def test_standard_has_no_special_draft(self):
  r=m.run_commander_dynamic_policy(waves=4,commander='standard',seed=2,policy='none')
  self.assertTrue(all(not x[3] for x in r['history']))
 def test_tander_normal_screen_has_four_cards(self):
  r=m.run_commander_dynamic_policy(waves=1,commander='tander',seed=2,policy='none')
  self.assertEqual(len(r['history'][0][1]),4)

class WaveStateTests(unittest.TestCase):
 def test_clean_lions_wave1_ticket_snapshot(self):
  s=m.doctrine_pool_snapshot('Lions',1,placed_families={0})
  self.assertEqual((s['ordinary_tickets'],s['desired_tb_tickets'],s['competing_tb_tickets'],s['total_tickets']),(38.0,6.0,0.0,44.0))
  self.assertAlmostEqual(s['desired_per_doctrine_draw'],6/44)
 def test_competing_family_adds_six_tickets(self):
  a=m.doctrine_pool_snapshot('Lions',1,placed_families={0})
  b=m.doctrine_pool_snapshot('Lions',1,placed_families={0,1})
  self.assertEqual(b['competing_tb_tickets']-a['competing_tb_tickets'],6.0)
 def test_started_removed_branch_persists_in_snapshot(self):
  s=m.doctrine_pool_snapshot('Lions',1,tb_owned={'TB0D1'},placed_families=set())
  self.assertEqual(s['desired_tb_tickets'],3.0)
 def test_tander_wave_opportunities(self):
  x=m.commander_wave_opportunities('tander',1)
  self.assertEqual(x['normal_candidates'],8); self.assertAlmostEqual(x['expected_normal_doctrine_candidates'],2.32)
 def test_magel_even_wave_adds_three_guaranteed_candidates(self):
  odd=m.commander_wave_opportunities('magel',1); even=m.commander_wave_opportunities('magel',2)
  self.assertEqual(odd['guaranteed_special_doctrine_candidates'],0); self.assertEqual(even['guaranteed_special_doctrine_candidates'],3)
  self.assertAlmostEqual(even['expected_total_doctrine_candidates'],4.74)

if __name__=='__main__': unittest.main(verbosity=2)

class SamplingTests(unittest.TestCase):
 def test_sampling_has_no_replacement(self):
  import random
  got=m.sample_doctrines(random.Random(1),[('A',1),('B',1),('C',1)],3)
  self.assertEqual(len(got),len(set(got)))
 def test_zero_doctrine_draws(self):
  import random
  self.assertEqual(m.sample_doctrines(random.Random(1),[('A',1)],0),[])
 def test_deployment_target_boundary(self):
  self.assertEqual(set(m.deployment_targets(6)),{'AMP_I','ATT_I'})
  self.assertEqual(set(m.deployment_targets(7)),{'AMP_I','ATT_I','AMP_II','ATT_II'})

class PolicyInvariantTests(unittest.TestCase):
 def test_t1_removal_is_heavier_early_than_t2(self):
  p=dict(m.wave_weights('Lions',7)); self.assertGreater(p['AMP_I'],p['AMP_II'])
 def test_more_families_increase_denominator(self):
  for w in (1,7,12,20,35):
   a=sum(x[1] for x in m.wave_weights('Lions',w,0,3)); b=sum(x[1] for x in m.wave_weights('Lions',w,1,3)); self.assertGreater(b,a)
 def test_denshikova_pollution_exceeds_normal(self):
  w=12; base=sum(x[1] for x in m.wave_weights('Lions',w,0,3)); normal=sum(x[1] for x in m.wave_weights('Lions',w,1,3))-base; densh=sum(x[1] for x in m.wave_weights('Lions',w,1,12))-base; self.assertGreater(densh,normal)

class BuildingAdmissionTests(unittest.TestCase):
 def test_current_tb_family_count(self):
  self.assertEqual(len(m.TB_FAMILIES),21)
 def test_cb12_is_pool_neutral(self):
  self.assertFalse(m.admits_tb_family('CB12'))
 def test_pargan_barricade_is_pool_neutral_t1(self):
  self.assertEqual(m.DOCTRINE_FREE_BUNDLE_BUILDINGS['F302'],1)
  self.assertFalse(m.admits_tb_family('F302'))
 def test_platform_is_pool_neutral_t1_utility(self):
  self.assertEqual(m.DOCTRINE_FREE_BUNDLE_BUILDINGS['SB06'],1)
  self.assertFalse(m.admits_tb_family('SB06'))
 def test_doctrine_free_tier_distribution(self):
  vals=list(m.DOCTRINE_FREE_BUNDLE_BUILDINGS.values())
  self.assertEqual((vals.count(1),vals.count(2),vals.count(3)),(2,3,6))

class SequentialPolicyTests(unittest.TestCase):
 def test_screen_has_six_slots_and_three_cards(self):
  import random
  c=m.doctrine_screen(random.Random(1),'Lions',1)
  self.assertEqual(len(c),3); self.assertEqual(sum(map(len,c)),6)
 def test_screen_doctrines_are_unique(self):
  import random
  for seed in range(100):
   c=m.doctrine_screen(random.Random(seed),'Lions',12)
   ds=[x for card in c for x in card if x]
   self.assertEqual(len(ds),len(set(ds)))
 def test_taken_doctrines_are_exhausted_next_wave(self):
  r=m.run_doctrine_policy(waves=2,seed=3)
  first=set(r['history'][0][4]); second=[x for c in r['history'][1][3] for x in c if x]
  self.assertTrue(first.isdisjoint(second))
 def test_pool_neutral_building_does_not_count_as_family(self):
  self.assertFalse(m.admits_tb_family('F302'))

class FastSequentialTests(unittest.TestCase):
 def test_cached_pool_matches_uncached(self):
  for w in (1,7,12,35):
   self.assertEqual(tuple(m.wave_weights('Lions',w,3,3)),m.cached_wave_weights('Lions',w,3,3))
 def test_fast_run_is_deterministic(self):
  a=m.run_doctrine_policy_fast(seed=99); b=m.run_doctrine_policy_fast(seed=99)
  self.assertEqual(a,b)

class PolicyV2Tests(unittest.TestCase):
 def test_tier_weight_accounting(self):
  self.assertEqual(m.doctrine_weight_at_wave('T1_9',12),100)
  self.assertEqual(m.doctrine_weight_at_wave('T2_9',12),12)
  self.assertEqual(m.doctrine_weight_at_wave('T3_9',12),2)
 def test_aggressive_prefers_t1_weight(self):
  import random
  cards=[['T2_9',None],['T1_9',None],[None,None]]
  got,_=m.choose_doctrine_card_v2(cards,'aggressive',random.Random(1),wave=12)
  self.assertEqual(got,['T1_9'])

class UtilityPolicyTests(unittest.TestCase):
 def test_resource_normalization(self):
  self.assertAlmostEqual(m.immediate_item_utility(('supply',139)),1)
  self.assertAlmostEqual(m.immediate_item_utility(('recon',34.25)),1)
 def test_cleanup_bonus_can_flip_choice(self):
  import random
  cards=[[('bp','X'),('bp','Y')],[('doctrine','T1_9'),('supply',100)],[('recon',25),('supply',100)]]
  a,_=m.choose_card_utility(cards,random.Random(1),wave=1,cleanup_bonus=0)
  b,_=m.choose_card_utility(cards,random.Random(1),wave=1,cleanup_bonus=2)
  self.assertEqual(a,0); self.assertEqual(b,1)

class TBProgressionTests(unittest.TestCase):
 def test_fresh_family_has_d1_d4(self):
  self.assertEqual(m.tb_active_nodes(0,set()),['TB0D1','TB0D4'])
  self.assertEqual(m.tb_active_nodes(0,set(),placed=False),[])
  self.assertEqual(m.tb_active_nodes(0,{'TB0D1'},placed=False),['TB0D2'])
  self.assertEqual(m.tb_active_nodes(0,{'TB0D1','TB0D2'},placed=False),['TB0D3'])
  self.assertEqual(m.tb_active_nodes(0,{'TB0D4'},placed=False),['TB0D5'])
  self.assertEqual(m.tb_active_nodes(0,{'TB0D1','TB0D2','TB0D3'},placed=False),['TB0D7'])
 def test_removed_family_pool_keeps_started_branch_only(self):
  pool=dict(m.dynamic_doctrine_pool_fast('Lions',1,tb_owned={'TB0D1'},placed_families=set()))
  self.assertIn('TB0D2',pool)
  self.assertNotIn('TB0D4',pool)
  self.assertNotIn('TB0D1',pool)
 def test_removed_family_pool_keeps_d7(self):
  pool=dict(m.dynamic_doctrine_pool_fast('Lions',1,tb_owned={'TB0D1','TB0D2','TB0D3'},placed_families=set()))
  self.assertIn('TB0D7',pool)
  self.assertNotIn('TB0D4',pool)
 def test_unstarted_removed_family_leaves_no_trace(self):
  base=dict(m.dynamic_doctrine_pool_fast('Lions',1,placed_families=set()))
  self.assertFalse(any(x.startswith('TB0D') for x in base))
 def test_branch_advances_without_cleaning_slot(self):
  self.assertEqual(m.tb_active_nodes(0,{'TB0D1'}),['TB0D2','TB0D4'])
  self.assertEqual(m.tb_active_nodes(0,{'TB0D1','TB0D2'}),['TB0D3','TB0D4'])
 def test_d7_or_unlock(self):
  got=m.tb_active_nodes(0,{'TB0D1','TB0D2','TB0D3'})
  self.assertEqual(got,['TB0D4','TB0D7'])
 def test_d7_taken_other_branch_remains(self):
  got=m.tb_active_nodes(0,{'TB0D1','TB0D2','TB0D3','TB0D7'})
  self.assertEqual(got,['TB0D4'])
 def test_family_fully_exhausted(self):
  owned={f'TB0D{i}' for i in range(1,8)}
  self.assertEqual(m.tb_active_nodes(0,owned),[])
