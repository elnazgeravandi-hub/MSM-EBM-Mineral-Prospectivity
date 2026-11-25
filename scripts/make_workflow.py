"""Figure 3: methodological workflow schematic (not a numeric result)."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    out=Path('outputs/synthetic_demo');out.mkdir(parents=True,exist_ok=True)
    steps=['12 evidence layers + fuzzy standardization', 'Positive/background labeled-cell construction',
    'Buffered spatial five-fold cross-validation', 'Four locked models + OOF performance',
    'Refit all labeled cells + full-area maps', 'Interpretation + descriptive enrichment',
    'Percentile threshold + DBSCAN targets']
    fig,ax=plt.subplots(figsize=(10,9));ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
    for i,step in enumerate(steps):
        y=.94-i*.135;ax.text(.5,y,step,ha='center',va='center',bbox=dict(boxstyle='round,pad=.7',fc='white',ec='black'))
        if i<len(steps)-1:ax.annotate('',xy=(.5,y-.094),xytext=(.5,y-.032),arrowprops=dict(arrowstyle='->'))
    fig.savefig(out/'Figure_03_WORKFLOW_SCHEMATIC.png',dpi=180,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':main()
