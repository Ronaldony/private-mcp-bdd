"""Synthetic record tests ONLY. No MCP server or network is exercised."""
from copy import deepcopy
from datetime import date
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('record_validator', ROOT/'scripts/validate_artifacts.py')
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
TODAY = date(2026, 9, 10)


def template():
    return json.loads((ROOT/'assets/project-manifest.template.json').read_text(encoding='utf-8'))


def synthetic_complete_record():
    """Fabricated fixture to exercise STRUCTURE; not a real release record."""
    data = template()
    data['project'] = dict(name='synthetic-fixture', owner='test-only', purpose='test validator',
                           non_goals=['no server validation'], data_classes=['synthetic'])
    data['compatibility'] = dict(era='modern', protocol_versions=['2026-07-28'],
                                transports=['stdio'], sdk={'name':'synthetic-sdk','pin':'test-commit-0001'},
                                hosts=[dict(name='synthetic-host',version='fixture-1',transport='stdio',
                                            evidence=['synthetic://not-real'])], extensions=[])
    data['profiles'] = ['P1']
    for control in data['controls']:
        control.update(decision='apply', rationale='Synthetic test only', owner='fixture',
                       status='verified', mechanism='Synthetic test only', evidence=['synthetic://not-real'])
    for test in data['tests']:
        test.update(applicable=True, status='pass', reason='Synthetic test only', evidence=['synthetic://not-real'])
    data['release'].update(decision='approved', reviewer='synthetic-fixture', reviewed_at=TODAY.isoformat())
    return data


class RecordValidatorTests(unittest.TestCase):
    def check(self, data, release=False):
        return module.validate(data, release_record=release, as_of=TODAY)

    def test_01_empty_template_is_valid_structure(self):
        self.assertEqual(self.check(template()), [])

    def test_02_empty_template_is_not_complete_release(self):
        self.assertTrue(self.check(template(), True))

    def test_03_synthetic_complete_record_structure(self):
        self.assertEqual(self.check(synthetic_complete_record(), True), [])

    def test_04_root_type(self):
        self.assertTrue(self.check([]))

    def test_05_missing_control(self):
        data = template(); data['controls'].pop()
        self.assertTrue(self.check(data))

    def test_06_duplicate_test(self):
        data = template(); data['tests'].append(deepcopy(data['tests'][0]))
        self.assertTrue(self.check(data))

    def test_07_unknown_id(self):
        data = template(); data['controls'][0]['id'] = 'C99'
        self.assertTrue(self.check(data))

    def test_08_failed_test_blocks_release(self):
        data = synthetic_complete_record(); data['tests'][0]['status'] = 'fail'
        self.assertTrue(self.check(data, True))

    def test_09_missing_evidence(self):
        data = synthetic_complete_record(); data['tests'][0]['evidence'] = []
        self.assertTrue(self.check(data, True))

    def test_10_conditional_test_not_applicable_review(self):
        data = synthetic_complete_record(); data['tests'][3].update(applicable=False,status='not_applicable',reason='Synthetic modern-only fixture')
        self.assertEqual(self.check(data, True), [])

    def test_11_universal_test_cannot_be_skipped(self):
        data = synthetic_complete_record(); data['tests'][0].update(applicable=False,status='not_applicable')
        self.assertTrue(self.check(data, True))

    def test_12_latest_sdk_not_pin(self):
        data = synthetic_complete_record(); data['compatibility']['sdk']['pin'] = 'latest'
        self.assertTrue(self.check(data, True))

    def test_13_expired_exception(self):
        data = synthetic_complete_record(); data['exceptions'] = [dict(id='EX1',kind='project_policy',controls=['C09'],reason='fixture',risk='fixture',compensating_control='fixture',approver='fixture',expires_at='2026-09-09',approved=True)]
        self.assertTrue(self.check(data, True))

    def test_14_protocol_exception_not_waived(self):
        data = synthetic_complete_record(); data['exceptions'] = [dict(id='EX1',kind='protocol_must',controls=['C02'],reason='fixture',risk='fixture',compensating_control='fixture',approver='fixture',expires_at='2026-09-11',approved=True)]
        self.assertTrue(self.check(data, True))

    def test_15_malformed_nested_records_no_crash(self):
        for field in ('project','compatibility','controls','tests','exceptions','release'):
            data = template(); data[field] = 7
            with self.subTest(field=field):
                self.assertTrue(self.check(data, True))

        for bad_id in ([], {}):
            data = template(); data['tests'][0]['id'] = bad_id
            with self.subTest(id_type=type(bad_id).__name__):
                self.assertTrue(self.check(data, True))

    def test_16_boolean_is_not_integer(self):
        data = synthetic_complete_record(); data['tests'][0]['applicable'] = 1
        self.assertTrue(self.check(data, True))

    def test_17_future_review(self):
        data = synthetic_complete_record(); data['release']['reviewed_at'] = '2026-09-11'
        self.assertTrue(self.check(data, True))

    def test_18_catalog_references(self):
        controls = json.loads((ROOT/'assets/control-matrix.json').read_text())['controls']
        tests = json.loads((ROOT/'assets/acceptance-tests.json').read_text())['tests']
        sources = json.loads((ROOT/'references/sources.json').read_text())
        self.assertEqual({c['id'] for c in controls}, module.CONTROL_IDS)
        self.assertEqual({t['id'] for t in tests}, module.TEST_IDS)
        source_ids = {s['id'] for s in sources}
        for c in controls:
            self.assertTrue(set(c['sources']) <= source_ids)
            self.assertTrue(set(c['tests']) <= module.TEST_IDS)
        for t in tests:
            self.assertTrue(set(t['controls']) <= module.CONTROL_IDS)


if __name__ == '__main__':
    unittest.main()
