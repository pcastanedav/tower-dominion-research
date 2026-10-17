"""Reproducible report for the conditional Wave-35 D7 pilot."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'docs/tasks/expertise-wave35'
POLICIES = ('isolated','minimal','moderate','broad','delayed','late')

def wilson(p,n,z=1.96):
    denom=1+z*z/n
    mid=(p+z*z/(2*n))/denom
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/denom
    return mid-half,mid+half

def render():
    lines=['# Wave-35 D7 Doctrine pilot — conditional results', '',
      'Target: `CB14` Rampart Missile Silo; faction: Lions; 1,000 paired seed IDs per commander/policy/mode.',
      '', '**Interpretation warning:** These are outputs from a provisional reward simulator, not measured game odds.',
      'D7 is reached after either D3 (cost branch) or D6 (efficiency branch). The exact localized target name remains unverified.',
      'All estimates use the user-approved earliest construction Wave 10; no cost model was used.', '',
      '## D7 acquisition by Wave 35 (percent)', '',
      '95% intervals use Wilson binomial intervals for each scenario; paired Eleonor differences below are point estimates, not paired confidence intervals.', '']
    for mode in ('guaranteed','modeled'):
        data=json.loads((ROOT/'pilot-d7'/f'{mode}.json').read_text())['scenarios']
        lines += [f'### {mode.title()} Blueprint mode','',
          '| Competing families | No Eleonor D7 (95% CI) | Eleonor D7 (95% CI) | Difference (pp) | Built: no Eleonor / Eleonor |',
          '|---|---:|---:|---:|---:|']
        for policy in POLICIES:
            a=data[f'{policy}/baseline']; b=data[f'{policy}/eleanor']; n=a['trials']
            def fmt(r):
                p=r['d7_completed']; lo,hi=wilson(p,n)
                return f'{p*100:.1f}% ({lo*100:.1f}–{hi*100:.1f})'
            lines.append(f'| {policy} | {fmt(a)} | {fmt(b)} | {(b["d7_completed"]-a["d7_completed"])*100:+.1f} | {a["constructed"]*100:.1f}% / {b["constructed"]*100:.1f}% |')
        lines += ['', '#### D7 unlock routes (completed runs)', '',
          '| Policy | No Eleonor: cost / efficiency / both | Eleonor: cost / efficiency / both |',
          '|---|---:|---:|']
        for policy in POLICIES:
            a=data[f'{policy}/baseline']['d7_routes']; b=data[f'{policy}/eleanor']['d7_routes']
            lines.append(f'| {policy} | {a["cost"]} / {a["efficiency"]} / {a["both"]} | {b["cost"]} / {b["efficiency"]} / {b["both"]} |')
        lines += ['', '#### Amplifier and Attenuator observations','',
          'Counts below aggregate across 1,000 runs per row. Offers include unselected ordinary cards and nested Doctrine drafts. Acquisitions are actual selections; no Attenuator targeting/use policy is modeled.', '',
          '| Policy / commander | Amplifier assigned runs | Amplifier saved runs | Amplifier offers / acquired | Attenuator offers / acquired | Runs with no Attenuator offer |',
          '|---|---:|---:|---:|---:|---:|']
        for policy in POLICIES:
            for commander in ('baseline','eleanor'):
                row=data[f'{policy}/{commander}']
                lines.append(f'| {policy} / {commander} | {row["amplifier_assigned_runs"]} | {row["amplifier_saved_runs"]} | {row["amplifier_offers"]} / {row["amplifier_acquired"]} | {row["attenuator_offers"]} / {row["attenuator_acquired"]} | {row["attenuator_zero_offer_runs"]} |')
        lines.append('')
    lines += ['## Important modeling boundaries','',
      '- Eleonor gets +20 raw Tier 2 and Tier 3 Blueprint weight and a provisional even-wave three-distinct-Blueprint draft; the exact in-game special-draft sampler remains unverified.',
      '- Competing families are counterfactual placements, not a modeled construction economy; each policy uses the same first eligible family IDs.',
      '- Two Amplifiers add +100% each to the target building-Doctrine raw weight; their Blueprint effect applies after assignment. Amplifier acquisition is opportunistic, not guaranteed.',
      '- Ordinary card scoring prioritizes an available Amplifier first, then D7 or the most advanced available branch, then the missing target Blueprint. The branch tie-break favors the cost route.',
      '- Some ordinary Doctrine effects and source-specific target Expertise labels remain unverified. Nested Doctrine choices are provisional.',
      '- A higher Eleonor result in modeled acquisition is consistent with faster Blueprint access; a small lower result in guaranteed mode may reflect divergent RNG and the extra draft, not a direct negative Doctrine modifier.',
      '- Wilson intervals quantify Monte Carlo sampling uncertainty only; they do not account for mechanical model uncertainty.', '',
      '## Reproduction','',
      '`PYTHONPATH=model python -m unittest model.test_expertise_wave35 -v`', '',
      '`PYTHONPATH=model python -m expertise_report`', '',
      'Input: `docs/tasks/expertise-wave35/pilot-d7/{guaranteed,modeled}.json`. Report generation does not resimulate.', '']
    return '\n'.join(lines)

if __name__ == '__main__':
    target=ROOT/'REPORT.md'
    target.write_text(render())
    print(target)
