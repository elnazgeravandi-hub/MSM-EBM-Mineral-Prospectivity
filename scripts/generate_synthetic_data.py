from pathlib import Path
from src.synthetic import create
if __name__=='__main__':
    p=Path('data/synthetic/demo.csv');p.parent.mkdir(parents=True,exist_ok=True)
    d=create();d.to_csv(p,index=False)
    print(f'Wrote {len(d)} artificial rows to {p}')
