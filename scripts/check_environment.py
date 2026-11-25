"""Safely report runtime versions and parameter API compatibility, without data."""
import importlib
import inspect
import json
from pathlib import Path
import yaml

def run():
    names={'numpy':'numpy','pandas':'pandas','scipy':'scipy','scikit-learn':'sklearn',
           'interpret-core':'interpret','catboost':'catboost'}
    results={}
    for display,package in names.items():
        try:
            mod=importlib.import_module(package)
            results[display]={'installed':True,'version':getattr(mod,'__version__','not exposed')}
        except ImportError as exc:
            results[display]={'installed':False,'error':str(exc)}
    cfg=yaml.safe_load(Path('configs/manuscript.yaml').read_text())
    if results['interpret-core']['installed']:
        from interpret.glassbox import ExplainableBoostingClassifier
        supported=set(inspect.signature(ExplainableBoostingClassifier).parameters)
        extra=set(cfg['models']['ebm'])|{'monotone_constraints','random_state'}
        results['ebm_parameter_compatibility']={'unsupported':sorted(extra-supported)}
    else:
        results['ebm_parameter_compatibility']='NOT TESTED: interpret-core missing'
    print(json.dumps(results,indent=2))
    return results

if __name__=='__main__':run()
