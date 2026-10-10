"""Provenance and conservative output lifecycle for MC experiments."""
import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def revision(root):
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def source_dirty(root):
    try:
        return bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, stderr=subprocess.DEVNULL, text=True).strip())
    except (OSError, subprocess.CalledProcessError):
        return None


def verify_completed(output):
    """Verify completion marker and checksums before consuming results."""
    output = Path(output)
    manifest = json.loads((output / 'run_manifest.json').read_text())
    if manifest.get('status') != 'completed':
        raise ValueError('run is not complete: %s' % manifest.get('status'))
    if manifest.get('completed_runs') != manifest.get('total_runs_planned'):
        raise ValueError('run completion count does not match planned runs')
    for name in ('raw.csv', 'results.json'):
        if not (output / name).is_file() or manifest.get('checksums', {}).get(name) != digest(output / name):
            raise ValueError('output checksum mismatch: %s' % name)
    return manifest


def write_atomic(path, payload):
    path = Path(path)
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('x') as f:
        json.dump(payload, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temporary, path)


def initialize(output, resolved, root):
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError('experiment output directory must be empty: %s' % output)
    output.mkdir(parents=True, exist_ok=True)
    manifest = {'status': 'running', 'started_at': timestamp(), 'finished_at': None,
                'model_version': 'mc_wave60', 'spec_schema_version': resolved['schema_version'],
                'source_revision': revision(root), 'source_dirty': source_dirty(root), 'python_version': platform.python_version(),
                'platform': platform.platform(), 'resolved_configuration': resolved,
                'seed_start': resolved['seed_start'], 'trials': resolved['trials'],
                'total_runs_planned': resolved['total_runs'], 'completed_runs': 0,
                'checksums': {}}
    try:
        write_atomic(output / 'run_manifest.json', manifest)
    except BaseException:
        raise
    return manifest


def update(output, manifest, *, status=None, completed_runs=None, error=None):
    if status is not None:
        manifest['status'] = status
        manifest['finished_at'] = timestamp()
    if completed_runs is not None:
        manifest['completed_runs'] = completed_runs
    if error is not None:
        manifest['error'] = str(error)
    if status == 'completed':
        manifest['checksums'] = {name: digest(Path(output) / name) for name in ('raw.csv', 'results.json')}
    write_atomic(Path(output) / 'run_manifest.json', manifest)
