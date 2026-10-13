"""Recompute publication outputs from full-precision archived records."""
import csv,json,math
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image
from checks import compare,compare_tails
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
def csvwrite(p,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def build(out):
    out.mkdir(exist_ok=True,parents=True)
    ref=read(ROOT/'results/reference.json');corpus=read(ROOT/'data/corpus.json');frag=read(ROOT/'results/fragility-reference.json')
    summaries=[];ledgers=[]
    for file,label in [('app.json','original'),('app-patched.json','patched')]:
        summary,ledger=compare(ref,corpus,read(ROOT/'results'/file),frag)
        assert summary==read(ROOT/'results'/('results-'+label+'.json')),label+' comparator differs'
        summaries.append(summary);ledgers.append(ledger)
    tails=compare_tails(ref,read(ROOT/'results/app-patched.json'))
    assert tails['checks']>0 and tails['checks']==tails['passed']
    assert tails==read(ROOT/'results/results-patched.tails.json')
    dump(out/'tail_checks.json',tails)
    before,after=summaries;old,rows=ledgers
    assert after['checks']==before['checks']==68461 and after['pass']==68461 and before['pass']==64256
    table=[]
    for q,s in sorted(after['quantities'].items()):
        b=before['quantities'][q]
        table.append(dict(measure=q.split('.')[0],quantity=q.split('.',1)[1],checks=s['checks'],passed_before=b['pass'],passed_after=s['pass'],largest_difference_before=b['max_difference'],largest_difference=s['max_difference'],undefined_mismatches_before=b['nonfinite_mismatches'],tolerance=s['tolerance']))
    table.append(dict(measure='ALL',quantity='TOTAL',checks=after['checks'],passed_before=before['pass'],passed_after=after['pass'],largest_difference_before='',largest_difference='',undefined_mismatches_before='',tolerance='quantity-specific'))
    csvwrite(out/'table1_by_quantity.csv',table)
    datasets=[]
    audit=read(ROOT/'data/dataset-audit.json')
    for d in audit:
        cs=[c for c in corpus if c['dataset']==d['dataset']];rr=[r for c in cs for r in c['rows']]
        assert len(cs)==d['configurations']
        datasets.append(dict(dataset=d['dataset'],configurations=len(cs),rows=len(rr),rows_with_zero_cell=sum(any(r[k]==0 for k in ['ai','bi','ci','di']) for r in rr),double_zero_or_double_all_event_rows=sum((r['ai']==r['ci']==0)or(r['bi']==r['di']==0) for r in rr),reason=d['reason']))
    csvwrite(out/'table2_datasets.csv',datasets)
    dump(out/'check_ledger.json',rows);dump(out/'before_check_ledger.json',old)
    n={}
    def add(k,v,source,transformation):n[k]=dict(value=v,source=source,transformation=transformation)
    add('checks',len(rows),'results/reference.json + app-patched.json + data/corpus.json + fragility-reference.json','count recomputed check ledger')
    add('passed',sum(r['passed'] for r in rows),'same records','sum passed comparisons')
    add('before_passed',sum(r['passed'] for r in old),'results/app.json + references','sum passed comparisons before fixes')
    add('fixes',7,'bench/fix.patch and results/HISTORICAL_RESULTS.md','static defect classification; not seven independent numerical groups')
    add('configurations',len(corpus),'data/corpus.json','count configurations')
    add('datasets_used',sum(d['configurations']>0 for d in datasets),'data/dataset-audit.json','count included datasets')
    add('datasets_enumerated',len(datasets),'data/dataset-audit.json','count all dataset records')
    for key in ['rows','rows_with_zero_cell','double_zero_or_double_all_event_rows']:add(key,sum(d[key] for d in datasets),'data/corpus.json','sum occurrences across configurations')
    expected=read(ROOT/'expected/paper_values.json')
    assert all(n[k]['value']==v for k,v in expected.items())
    dump(out/'numbers.json',n)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.titlesize':9,'axes.labelsize':8,'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8})
    # Each point is the maximum observed difference within a named quantity.
    fig,axs=plt.subplots(4,1,figsize=(170/25.4,13),layout='constrained')
    for ax,m in zip(axs,['OR','RR','RD','PETO']):
        qs=[q for q in sorted(after['quantities']) if q.startswith(m+'.')]
        for i,q in enumerate(qs):
            b=before['quantities'][q];a=after['quantities'][q]
            ax.scatter(i,math.log10(max(a['max_difference'],1e-16)),s=14,color='#24658a',zorder=3)
            ax.scatter(i,math.log10(max(b['max_difference'],1e-16)),marker='x' if b['pass']<b['checks'] else '.',s=25,color='#bc552c',zorder=3)
            ax.plot([i-.35,i+.35],[math.log10(a['tolerance'])]*2,'--',color='#555',lw=1)
            if b['nonfinite_mismatches']:ax.scatter(i,1,marker='^',s=18,color='#bc552c')
        ax.set_title(m);ax.set_xticks(range(len(qs)),[q.split('.',1)[1] for q in qs],rotation=90)
        top=max(2,math.ceil(max(math.log10(max(before['quantities'][q]['max_difference'],1e-16)) for q in qs))+.5)
        ax.set_ylabel('log10 maximum difference');ax.set_ylim(-17,top);ax.grid(axis='y',alpha=.2)
    fig.suptitle('MH/Peto agreement by quantity\nBlue: after; orange: before; x: failures; triangle: undefined mismatch\nDashed: tolerance. Relative differences except p / rounded UI. Zeros at -16.',fontsize=9)
    save(fig,out,'figure2_agreement');plt.close(fig)
    fig=plt.figure(figsize=(170/25.4,3.65))
    boxes=[('Problem','Rare-event\n2 x 2 tables\nneed reliable\npooling.'),('Tool','Browser MH\nOR / RR / RD\nand Peto OR\nwith diagnostics.'),('Validation',f"{n['datasets_used']['value']} datasets\n{len(corpus)} configurations\nAgainst R package\nmetafor."),('Result',f"{n['passed']['value']:,} of {n['checks']['value']:,}\nchecks pass\n(after {n['fixes']['value']} fixes)")]
    for i,(head,body) in enumerate(boxes):
        x=.02+i*.245;fig.patches.append(FancyBboxPatch((x,.25),.22,.52,boxstyle='round,pad=0.008',transform=fig.transFigure,facecolor=['#f4ece8','#e8f0f7','#eaf4ec','#fdf6e3'][i],edgecolor='#999'))
        fig.text(x+.11,.70,head,ha='center',weight='bold',fontsize=10);fig.text(x+.11,.49,body,ha='center',va='center',fontsize=8,linespacing=1.6)
    fig.text(.5,.89,'Mantel-Haenszel and Peto in the browser',ha='center',fontsize=11,weight='bold')
    fig.text(.5,.13,'Numerical, rounded UI and structural checks; metafor 5.2-1.',ha='center',fontsize=8)
    fig.text(.5,.07,'Computational regroupings are not clinical analyses.',ha='center',fontsize=8)
    save(fig,out,'visual_abstract');plt.close(fig)
    sizes={}
    for p in sorted(out.iterdir()):
        if p.suffix in ['.png','.tif']:
            with Image.open(p) as im:sizes[p.name]=dict(width_pixels=im.width,height_pixels=im.height,dpi=list(map(float,im.info['dpi'])))
    dump(out/'sizes.json',sizes)
    report='# Reproduction report\n\n'
    report+='Comparisons are recomputed from app and R records; expected numbers are assertions only.\n\n'
    report+='Figure 2 plots per-quantity finite maxima (relative except p-values and rounded UI); undefined mismatches are triangles. Exact zeros and differences below 1e-16 are plotted at -16. All text is at least 8 pt; images are 300 dpi, nominal width 170 mm. Tables include all checks, including archived UI/refusal evidence.\n\n'
    report+='| Element | Static / dynamic | Source |\n|---|---|---|\n| Tolerances and seven-defect classification | Static | bench/compare.py and historical report |\n| Counts, differences, plots and verdicts | Dynamic | Full-precision records, analysis/checks.py |\n| Expected totals | Static assertions | expected/paper_values.json |\n\n'
    final=f"PASS: {len(expected)}/{len(expected)} paper-value assertions; {after['pass']}/{after['checks']} final checks; {before['pass']}/{before['checks']} before fixes."
    (out/'reproduction_report.md').write_text(report+final+'\n',encoding='utf-8');print(final)
def save(fig,out,name):
    for ext in ['png','tif']:fig.savefig(out/(name+'.'+ext),dpi=300)
if __name__=='__main__':build(ROOT/'outputs')
