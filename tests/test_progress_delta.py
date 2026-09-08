import importlib.util, json, tempfile, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class ProgressDeltaTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        (self.root/'scripts').mkdir(); (self.root/'survey-state/cycle-plans').mkdir(parents=True)
        (self.root/'survey-state/runs').mkdir(parents=True)
        (self.root/'scripts/cycle_state.py').write_text((HERE/'scripts/cycle_state.py').read_text())
        (self.root/'scripts/progress_delta.py').write_text((HERE/'scripts/progress_delta.py').read_text())
        plan={'plan_id':'c1','target':1,'audit_target':1,
              'selected_papers':[{'canonical_id':'R1','status':'pending'}],
              'selected_audits':[{'canonical_id':'A1','status':'pending'}]}
        (self.root/'survey-state/cycle-plans/cycle-000001.json').write_text(json.dumps(plan))
        st={'schema_version':1,'workflow_version':8,'cycle_number':1,'cycle_id':'cycle-000001','max_runs':24,
            'next_run_index':2,'active_claim':{'cycle_id':'cycle-000001','run_index':2,'run_id':'r','claim_token':'t','workflow_commit':'abcdef1'},
            'targets':{'research':1,'audit':1},'current_plan_id':'c1','current_plan_path':'survey-state/cycle-plans/cycle-000001.json'}
        (self.root/'survey-state/cycle-state.json').write_text(json.dumps(st))
        self.mod=load(self.root/'scripts/progress_delta.py','progress_test'); self.mod.ROOT=self.root
    def tearDown(self): self.tmp.cleanup()
    def test_small_delta_marks_logical_completion(self):
        out=self.mod.prepare('research','R1','completed','added','r','t',['paper.md'],['abc'],None,True)
        self.assertTrue((self.root/out['path']).exists())
        cycle=load(self.root/'scripts/cycle_state.py','cycle_status')
        st=json.loads((self.root/'survey-state/cycle-state.json').read_text())
        self.assertEqual(cycle.apply_progress(self.root,st)['research']['pending'],0)
    def test_stale_claim_rejected(self):
        with self.assertRaises(ValueError):
            self.mod.prepare('research','R1','completed','added','r','old',[],[],None,False)

if __name__=='__main__': unittest.main()
