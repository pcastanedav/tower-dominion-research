#!/usr/bin/env python3
"""Human-friendly standalone workflow for reproducible MC experiments."""
import argparse
import json
import shutil
import sys
from pathlib import Path
from mc_agent_interface import execute, capabilities
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
PRESETS = ROOT / 'presets' / 'mc'


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('capabilities', help='Show supported fields and metrics')
    commands.add_parser('presets', help='List bundled starter experiments')
    init = commands.add_parser('init', help='Copy a preset to an editable JSON spec')
    init.add_argument('preset')
    init.add_argument('--config', type=Path, required=True)
    for command in ('validate', 'preview', 'run'):
        sub = commands.add_parser(command)
        sub.add_argument('--config', type=Path, required=True)
        if command == 'run':
            sub.add_argument('--output', type=Path, required=True)
            sub.add_argument('--report', choices=['none', 'markdown', 'pdf', 'both'], default='both')
    report = commands.add_parser('report', help='Generate reports for a completed run')
    report.add_argument('--output', type=Path, required=True)
    report.add_argument('--format', choices=['markdown', 'pdf', 'both'], default='both')
    args = parser.parse_args()
    try:
        if args.command == 'capabilities':
            data = capabilities()
            print(json.dumps(data, indent=2, default=str))
        elif args.command == 'presets':
            for preset in sorted(PRESETS.glob('*.json')):
                spec = json.loads(preset.read_text())
                print('%s — %s' % (preset.stem, spec.get('question', '')))
        elif args.command == 'init':
            source = PRESETS / (args.preset + '.json')
            if args.preset != Path(args.preset).name or not source.is_file():
                raise ValueError('Unknown preset %r; use presets to list available names' % args.preset)
            with args.config.open('x') as target:
                target.write(source.read_text())
            print('Created %s' % args.config)
        elif args.command in ('validate', 'preview'):
            result = execute(SimpleNamespace(operation=args.command, config=args.config))
            print(json.dumps(result, indent=2, default=str))
        elif args.command == 'run':
            result = execute(SimpleNamespace(operation='run', config=args.config, output=args.output))
            print('Completed %s runs across %s scenarios in %s' % (result['total_runs'], result['scenario_count'], args.output))
            if args.report != 'none':
                artifacts = execute(SimpleNamespace(operation='report', output=args.output, format=args.report))['artifacts']
                print('Reports: %s' % ', '.join(artifacts))
        elif args.command == 'report':
            result = execute(SimpleNamespace(operation='report', output=args.output, format=args.format))
            print('Reports: %s' % ', '.join(result['artifacts']))
    except (ValueError, OSError, RuntimeError, KeyError, json.JSONDecodeError) as error:
        print('Error: %s' % error, file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(cli())
