import importlib.util, json, tempfile, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class CycleStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        (self.root/'scripts').mkdir(); (self.root/'survey-state/daily-plans').mkdir(parents=True)
        (self.root/'survey-state/runs').mkdir(parents=True); (self.root/'survey-state/progress-deltas').mkdir(parents=True)
        (self.root/'scripts/cycle_state.py').write_text((HERE/'scripts/cycle_state.py').read_text())
        (self.root/'survey-state/leases.json').write_text(json.dumps({'schema_version':2,'workflow_version':8,'items':{}}))
        plan={'plan_id':'p1','target':2,'audit_target':2,
              'selected_papers':[{'canonical_id':'R1','status':'pending'},{'canonical_id':'R2','status':'pending'}],
              'selected_audits':[{'canonical_id':'A1','status':'pending'},{'canonical_id':'A2','status':'pending'}]}
        (self.root/'survey-state/daily-plans/p1.json').write_text(json.dumps(plan))
        st={'schema_version':1,'workflow_version':8,'cycle_number':1,'cycle_id':'cycle-000001','max_runs':24,
            'next_run_index':2,'active_claim':None,'targets':{'research':2,'audit':2},
            'current_plan_id':'p1','current_plan_path':'survey-state/daily-plans/p1.json'}
        (self.root/'survey-state/cycle-state.json').write_text(json.dumps(st))
        self.mod=load(self.root/'scripts/cycle_state.py','cycle_test')
    def tearDown(self): self.tmp.cleanup()
    def delta(self,side,cid,token):
        p=self.root/'survey-state/progress-deltas/cycle-000001'/side/(cid+'.json'); p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps({'schema_version':1,'workflow_version':8,'cycle_id':'cycle-000001','plan_id':'p1',
                                 'side':side,'canonical_id':cid,'status':'completed','run_id':'r','run_index':2,'claim_token':token}))
    def test_mode_from_counter_not_time(self):
        out=self.mod.claim(self.root,'r','abcdef1',scheduled_at='2099-01-01T00:00:00+09:00',apply=True)
        self.assertEqual((out['run_index'],out['mode']),(2,'reading'))
    def test_early_rollover_increments_targets(self):
        out=self.mod.claim(self.root,'r','abcdef1',apply=True)
        for side,ids in [('research',['R1','R2']),('audit',['A1','A2'])]:
            for cid in ids: self.delta(side,cid,out['claim_token'])
        done=self.mod.finish(self.root,'r',out['claim_token'],apply=True)
        self.assertTrue(done['early_rollover']); self.assertEqual(done['next_run_index'],1)
        st=json.loads((self.root/'survey-state/cycle-state.json').read_text())
        self.assertEqual(st['targets'],{'research':3,'audit':3})
    def test_run24_decrements_incomplete_sides(self):
        st=json.loads((self.root/'survey-state/cycle-state.json').read_text()); st['next_run_index']=24
        (self.root/'survey-state/cycle-state.json').write_text(json.dumps(st))
        out=self.mod.claim(self.root,'r24','abcdef1',apply=True)
        self.mod.finish(self.root,'r24',out['claim_token'],apply=True)
        st=json.loads((self.root/'survey-state/cycle-state.json').read_text())
        self.assertEqual(st['targets'],{'research':1,'audit':1})
    def test_claim_token_controls_lease(self):
        out=self.mod.claim(self.root,'r','abcdef1',apply=True)
        self.mod.work_claim(self.root,'paper:R1','r',out['claim_token'],'acquire',apply=True)
        self.mod.finish(self.root,'r',out['claim_token'],apply=True)
        self.assertEqual(json.loads((self.root/'survey-state/leases.json').read_text())['items'],{})

if __name__=='__main__': unittest.main()
