#!/usr/bin/env python3
"""Validate design/release RECORD structure, never an MCP server.

No network access, subprocesses, server calls, or evidence fetching are performed.
A successful result does not establish protocol conformance or security.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import sys
from typing import Any

VERSION = '0.1.0'
CONTROL_IDS = {f'C{i:02}' for i in range(1, 17)}
TEST_IDS = {f'T{i:02}' for i in range(1, 37)}
ALWAYS_TESTS = {'T01', 'T02', 'T30', 'T31', 'T33', 'T34', 'T35', 'T36'}
MAX_FILE_BYTES = 4 * 1024 * 1024


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def strings(value: Any, required: bool = False) -> bool:
    return (isinstance(value, list)
            and (not required or bool(value))
            and all(nonempty(v) for v in value))


def iso_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        result = date.fromisoformat(value)
        return result if value == result.isoformat() else None
    except ValueError:
        return None


def validate(data: Any, *, release_record: bool = False,
             as_of: date | None = None) -> list[str]:
    """Return human-readable structural errors without changing the input."""
    errors: list[str] = []
    today = as_of or date.today()
    if not isinstance(data, dict):
        return ['root: expected JSON object']

    def require(ok: bool, message: str) -> None:
        if not ok:
            errors.append(message)

    def section(name: str) -> dict[str, Any]:
        value = data.get(name)
        if not isinstance(value, dict):
            errors.append(f'{name}: expected object')
            return {}
        return value

    def text_fields(obj: dict[str, Any], fields: tuple[str, ...],
                    prefix: str, filled: bool = False) -> None:
        for key in fields:
            value = obj.get(key)
            require(nonempty(value) if filled else isinstance(value, str),
                    f'{prefix}.{key}: expected {"nonempty " if filled else ""}string')

    def records(name: str, expected: set[str]) -> list[dict[str, Any]]:
        value = data.get(name)
        if not isinstance(value, list):
            errors.append(f'{name}: expected array')
            return []
        valid = []
        ids: list[str] = []
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                errors.append(f'{name}[{index}]: expected object')
                continue
            key = item.get('id')
            if not isinstance(key, str):
                errors.append(f'{name}[{index}].id: expected string')
            else:
                ids.append(key)
            valid.append(item)
        require(len(ids) == len(set(ids)), f'{name}: duplicate IDs')
        missing = sorted(expected - set(ids))
        unknown = sorted(set(ids) - expected)
        require(not missing, f'{name}: missing IDs {missing}')
        require(not unknown, f'{name}: unknown IDs {unknown}; add business tests in a separate appendix')
        return valid

    require(data.get('schema_version') == VERSION,
            f'schema_version: expected {VERSION}')
    project = section('project')
    text_fields(project, ('name', 'owner', 'purpose'), 'project', release_record)
    for field in ('non_goals', 'data_classes'):
        require(strings(project.get(field), release_record),
                f'project.{field}: expected string array' + (' with entries' if release_record else ''))

    compatibility = section('compatibility')
    require(compatibility.get('era') in (('modern', 'legacy', 'dual-era') if release_record
                                         else ('', 'modern', 'legacy', 'dual-era')),
            'compatibility.era: expected modern, legacy, or dual-era')
    for field in ('protocol_versions', 'transports', 'extensions'):
        required = release_record and field != 'extensions'
        require(strings(compatibility.get(field), required),
                f'compatibility.{field}: expected string array')
    versions = compatibility.get('protocol_versions')
    if isinstance(versions, list):
        for version in versions:
            require(iso_date(version) is not None,
                    'compatibility.protocol_versions: use YYYY-MM-DD dates')
    transports = compatibility.get('transports')
    if isinstance(transports, list):
        for transport in transports:
            require(isinstance(transport, str) and transport in
                    ('stdio', 'streamable-http', 'legacy-http-sse'),
                    'compatibility.transports: unsupported record label')
    sdk = compatibility.get('sdk')
    if not isinstance(sdk, dict):
        errors.append('compatibility.sdk: expected object')
    else:
        text_fields(sdk, ('name', 'pin'), 'compatibility.sdk', release_record)
        if release_record:
            require(sdk.get('pin') not in ('latest', '*', 'main', 'master', 'HEAD'),
                    'compatibility.sdk.pin: provide a reviewed version or immutable commit')
    hosts = compatibility.get('hosts')
    require(isinstance(hosts, list), 'compatibility.hosts: expected array')
    if isinstance(hosts, list):
        require(not release_record or bool(hosts), 'compatibility.hosts: at least one tested host required')
        for i, host in enumerate(hosts):
            if not isinstance(host, dict):
                errors.append(f'compatibility.hosts[{i}]: expected object')
                continue
            text_fields(host, ('name', 'version', 'transport'), f'compatibility.hosts[{i}]', release_record)
            require(strings(host.get('evidence'), release_record),
                    f'compatibility.hosts[{i}].evidence: expected evidence string array')
    profiles = data.get('profiles')
    require(strings(profiles, release_record), 'profiles: expected string array')
    if isinstance(profiles, list):
        require(all(isinstance(p, str) and p in {f'P{i}' for i in range(1, 8)} for p in profiles),
                'profiles: use P1 through P7')

    for item in records('controls', CONTROL_IDS):
        label = f'control {item.get("id", "?")}'
        require(item.get('decision') in ('undecided', 'apply', 'not_applicable'),
                f'{label}.decision: invalid value')
        require(item.get('status') in ('planned', 'implemented', 'verified'),
                f'{label}.status: invalid value')
        text_fields(item, ('rationale', 'owner', 'mechanism'), label, release_record)
        require(strings(item.get('evidence'), release_record), f'{label}.evidence: expected evidence string array')
        if release_record:
            require(item.get('decision') != 'undecided', f'{label}: applicability is undecided')
            require(item.get('status') == 'verified', f'{label}: decision/control must be verified in submitted record')

    for item in records('tests', TEST_IDS):
        label = f'test {item.get("id", "?")}'
        applicable = item.get('applicable')
        require(applicable is None or isinstance(applicable, bool),
                f'{label}.applicable: expected true, false, or null')
        require('applicable' in item, f'{label}.applicable: missing')
        require(item.get('status') in ('not_run', 'pass', 'fail', 'skip', 'not_applicable'),
                f'{label}.status: invalid value')
        text_fields(item, ('reason',), label)
        require(strings(item.get('evidence')), f'{label}.evidence: expected string array')
        if release_record:
            require(isinstance(applicable, bool), f'{label}: applicability not decided')
            if isinstance(item.get('id'), str) and item['id'] in ALWAYS_TESTS:
                require(applicable is True, f'{label}: universal review/test cannot be marked not applicable')
            if applicable is True:
                require(item.get('status') == 'pass', f'{label}: applicable test must be recorded as pass')
                require(strings(item.get('evidence'), True), f'{label}: passing test needs evidence reference')
            elif applicable is False:
                require(item.get('status') == 'not_applicable', f'{label}: use not_applicable status')
                require(nonempty(item.get('reason')), f'{label}: non-applicability needs rationale')
                require(strings(item.get('evidence'), True), f'{label}: non-applicability needs review evidence')

    exceptions = data.get('exceptions')
    require(isinstance(exceptions, list), 'exceptions: expected array')
    if isinstance(exceptions, list):
        for i, item in enumerate(exceptions):
            label = f'exceptions[{i}]'
            if not isinstance(item, dict):
                errors.append(f'{label}: expected object')
                continue
            text_fields(item, ('id', 'reason', 'risk', 'compensating_control', 'approver', 'expires_at'),
                        label, release_record)
            require(item.get('kind') == 'project_policy',
                    f'{label}.kind: only project_policy exceptions; do not waive protocol conformance')
            require(strings(item.get('controls'), True), f'{label}.controls: expected control IDs')
            linked = item.get('controls')
            if isinstance(linked, list):
                require(all(isinstance(c, str) and c in CONTROL_IDS for c in linked),
                        f'{label}.controls: unknown ID')
            expiry = iso_date(item.get('expires_at'))
            require(expiry is not None, f'{label}.expires_at: use YYYY-MM-DD')
            if release_record:
                require(item.get('approved') is True, f'{label}: approval not recorded')
                require(expiry is not None and expiry >= today, f'{label}: exception expired')

    release = section('release')
    require(release.get('decision') in ('blocked', 'review', 'approved'), 'release.decision: invalid value')
    text_fields(release, ('reviewer', 'reviewed_at', 'notes'), 'release')
    if release_record:
        require(release.get('decision') == 'approved', 'release.decision: not approved in submitted record')
        require(nonempty(release.get('reviewer')), 'release.reviewer: reviewer required')
        reviewed = iso_date(release.get('reviewed_at'))
        require(reviewed is not None and reviewed <= today,
                'release.reviewed_at: valid non-future date required')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--release-record', action='store_true',
                        help='check completed release RECORD fields, not runtime readiness')
    parser.add_argument('--as-of', type=str, help='YYYY-MM-DD for record expiry checks; default is local date')
    args = parser.parse_args()
    as_of = iso_date(args.as_of) if args.as_of else date.today()
    if as_of is None:
        parser.error('--as-of must be YYYY-MM-DD')
    try:
        if args.manifest.stat().st_size > MAX_FILE_BYTES:
            raise ValueError('manifest exceeds 4 MiB record limit')
        data = json.loads(args.manifest.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError) as exc:
        print(f'INPUT ERROR: {exc}', file=sys.stderr)
        return 2
    errors = validate(data, release_record=args.release_record, as_of=as_of)
    if errors:
        print(f'RECORD CHECK FAILED: {len(errors)} structural/completeness issue(s)')
        for message in errors:
            print(f'- {message}')
        return 1
    mode = 'RELEASE RECORD COMPLETE' if args.release_record else 'STRUCTURE OK (draft fields may be empty)'
    print(mode)
    print('NOT a server test, security certification, or verification of evidence authenticity.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
