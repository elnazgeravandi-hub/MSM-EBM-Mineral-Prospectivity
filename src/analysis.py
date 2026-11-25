"""Analyses independent from private data and fitted model internals."""
import numpy as np
import pandas as pd
from .mapping import targets, jaccard, percentile_rank

def descriptive_enrichment(full_df, scores_by_model, enrichment_cell_ids, fractions=(.10,.20,.40,.50)):
    """Table 8: shares of unique descriptive cells captured in top ranked full-area fractions.
    The caller MUST supply non-training enrichment cell ids; these are not external validation.
    """
    cell_ids=full_df.cell_id.to_numpy()
    if len(set(cell_ids)) != len(cell_ids): raise ValueError('duplicate full-area cell ID')
    enriched=set(enrichment_cell_ids)
    if not enriched: raise ValueError('no enrichment cells')
    missing=enriched-set(cell_ids)
    if missing: raise ValueError('enrichment ID absent from grid')
    mask=np.isin(cell_ids,list(enriched))
    rows=[]
    for name,scores in scores_by_model.items():
        if len(scores)!=len(cell_ids): raise ValueError('score length mismatch')
        r=percentile_rank(scores)
        row={'model':name,'enrichment_count':int(mask.sum())}
        for fraction in fractions:
            row[f'top_{round(fraction*100)}_pct_capture']=100*np.mean(r[mask]>=100*(1-fraction))
        rows.append(row)
    return pd.DataFrame(rows)

def target_sensitivity(full_df, scores):
    """Table 9: 3 area thresholds x 3 eps + min_samples=2, including best-match count."""
    ref=targets(full_df,scores,.10,1.5,1)
    ref_top=ref[:10]
    footprint=lambda groups: set().union(*(set(t['cell_ids']) for t in groups))
    ref_ids=footprint(ref_top)
    rows=[]
    for frac,eps,minimum in [(f,e,1) for f in (.05,.10,.15) for e in (1.,1.5,2.)]+[(.10,1.5,2)]:
        alt=targets(full_df,scores,frac,eps,minimum)
        top=alt[:10]
        matched=0
        for target in ref_top:
            if not alt: continue
            similarities=[jaccard(target['cell_ids'],t['cell_ids']) for t in alt]
            if max(similarities)>0 and int(np.argmax(similarities))<10: matched+=1
        rows.append(dict(top_fraction=frac,eps=eps,min_samples=minimum,clusters=len(alt),
          top10_area_km2=sum(t['area_km2'] for t in top),
          footprint_jaccard=jaccard(ref_ids,footprint(top)),reference_targets_matched=matched,
          reference_target_count=len(ref_top)))
    return pd.DataFrame(rows)

def require_no_enrichment_overlap(labeled_df, enrichment_ids):
    overlap=set(labeled_df.cell_id).intersection(enrichment_ids)
    if overlap: raise ValueError(f'enrichment overlaps training/validation data: {len(overlap)} cells')
