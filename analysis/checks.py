import math,re
def compare(reference, configurations, apps, frag):
    refs={r['id']:r for r in reference}
    corpus={c['id']:c for c in configurations}
    assert len(refs)==len(reference)==4*len(corpus)
    assert len(apps)==3*len(corpus) and {a['id'] for a in apps}=={c+'|'+m for c in corpus for m in ['OR','RR','RD']}
    assert {f['id'] for f in frag}=={c+'|'+m for c,v in corpus.items() if len(v['rows'])>=2 for m in ['OR','RR','RD']}
    stats={};failures=[];skips=[];ledger=[]
    def check(q,a,b,id,tol=1e-9,absolute=False):
        s=stats.setdefault(q,{'checks':0,'pass':0,'max_difference':0,'nonfinite_mismatches':0,'tolerance':tol})
        s['checks']+=1
        if a is None or b is None: diff=0 if a is None and b is None else math.inf
        else: diff=abs(a-b)/(1 if q.endswith('.p') or absolute else max(1,abs(b)))
        if not math.isfinite(diff): diff=math.inf
        ok=diff<=tol;s['pass']+=ok
        ledger.append(dict(configuration=id,quantity=q,app=a,reference=b,difference=diff if math.isfinite(diff) else None,tolerance=tol,passed=ok))
        if math.isfinite(diff):s['max_difference']=max(s['max_difference'],diff)
        else:s['nonfinite_mismatches']+=1
        if not ok: failures.append({'id':id,'quantity':q,'app':a,'reference':b,'difference':diff if math.isfinite(diff) else None})
    def finite(x):return x if x is not None and math.isfinite(x) else None
    for a in apps:
        r=refs[a['id']];m=a['id'].rsplit('|',1)[1];res=a['result']
        if r['k_input']<2:
            skips.append({'id':a['id'],'reason':'Page requires >=2 input rows; R accepts a single row','page_refused':res is None})
            check(m+'.single_row_refusal',int(res is None),1,a['id'])
            check(m+'.single_row_UI_clear',int(not a['pooledText'] and not a['studyText']),1,a['id'])
            continue
        for method in ([m,'PETO'] if m=='OR' else [m]):
            rr=refs[a['id'].rsplit('|',1)[0]+'|'+method];prefix='peto' if method=='PETO' else 'mh'
            for k,v in [('est','est'),('lo','lo'),('hi','hi'),('z','zval'),('p','pval')]:check(method+'.'+k,res.get(prefix+'_'+k) if res else None,rr.get(v),a['id'])
            # SE and coefficient recovered algebraically from the full-precision exported CI.
            lo=res.get(prefix+'_lo') if res else None; hi=res.get(prefix+'_hi') if res else None;est=res.get(prefix+'_est') if res else None
            beta=(est if m=='RD' else math.log(est)) if est is not None and est>0 else (est if m=='RD' else None)
            se=((hi-lo) if m=='RD' else math.log(hi)-math.log(lo))/(2*1.959963984540054) if lo is not None and hi is not None and (m=='RD' or lo>0 and hi>0) else None
            check(method+'.beta',finite(beta),rr.get('beta'),a['id']);check(method+'.se',finite(se),rr.get('se'),a['id'])
        for line in a['pooledText'].splitlines():
            cells=line.split('\t');method='PETO' if cells[0]=='Peto OR' else m
            rr=refs[a['id'].rsplit('|',1)[0]+'|'+method]
            values=re.findall(r'-?\d+(?:\.\d+)?',' '.join(cells[1:]))
            if len(values)==5:
                for q,v in zip(['est','lo','hi','zval','pval'],values):check(method+'.display_pooled_'+q,float(v),rr.get(q),a['id'],tol=.0050000001 if q=='zval' else .0005000001,absolute=True)
        ss=a['studies'];rs=r.get('studies',[]);rows=corpus[a['id'].rsplit('|',1)[0]]['rows']
        expected_bus=[t for t in rs if t['se'] is not None and t['se']>0 and t['beta'] is not None]
        check(m+'.study_count',len(ss),len(expected_bus),a['id'])
        bylabel={'source-row-'+str(row['source_row']):i for i,row in enumerate(rows)}
        returned={s['label']:s for s in ss}
        for label,i in bylabel.items():
            t=rs[i]
            if t['se'] is None or t['se']<=0 or t['beta'] is None:continue
            s=returned.get(label,{})
            check(m+'.study_beta',s.get('est'),t['beta'],a['id']+f'|row{i+1}')
            check(m+'.study_se',s.get('se'),t['se'],a['id']+f'|row{i+1}')
        for i,line in enumerate(a['studyText'].splitlines()):
            cells=line.split('\t');t=rs[i]
            values=re.findall(r'-?\d+(?:\.\d+)?',cells[3]+' '+cells[4])
            if len(values)==3:
                for q,v in zip(['est','lo','hi'],values):check(m+'.display_study_'+q,float(v),t[q],a['id']+f'|row{i+1}',tol=.0005000001,absolute=True)
            else:
                check(m+'.display_study_defined',len(values),3,a['id']+f'|row{i+1}')
        if a['labbe']:
            check(m+'.labbe_logEff',a['labbe']['logEff'],r['labbe']['logEff'],a['id'])
            for i,p in enumerate(a['labbe']['points']):
                for q in ['pc','pt']:check(m+'.labbe_'+q,p[q],r['labbe'][q][i],a['id'])
            eff=r['labbe']['eff'];deltas=[]
            for p in a['labbe']['curve']:
                expected=eff*p['pc'] if m=='RR' else eff*p['pc']/(1-p['pc']+eff*p['pc'])
                deltas.append(abs(p['pt']-expected))
            check(m+'.labbe_curve_max_abs_error',max(deltas,default=0),0,a['id'])
    if frag:
        fr={r['id']:r for r in frag}
        for a in apps:
            if a['id'] not in fr:continue
            r=fr[a['id']];f=a.get('frag') or {};m=a['id'].rsplit('|',1)[1]
            for key in ['FI','FQ']:check(m+'.fragility_'+key,f.get(key),r[key],a['id'])
            for key,rkey in [('est','beta'),('lo','lo'),('hi','hi')]:check(m+'.fragility_DL_'+rkey,(f.get('pooled') or {}).get(key),r[rkey],a['id'])
    result={'quantities':stats,'failures':failures,'single_row_scope_exclusions':skips,'page_configurations':len(apps),'expected_page_configurations':len(corpus)*3,'fragility_configurations':len(fr) if frag else 0,'checks':sum(s['checks'] for s in stats.values()),'pass':sum(s['pass'] for s in stats.values())}
    return result,ledger


def compare_tails(reference, apps):
    refs={r['id']:r for r in reference};rows=[]
    for app in apps:
        base,m=app['id'].rsplit('|',1)
        if refs[app['id']]['k_input']<2:continue
        for method in ([m,'PETO'] if m=='OR' else [m]):
            ref=refs[base+'|'+method];b=ref.get('pval')
            if b is None or not 0<=b<1e-12:continue
            a=(app.get('result') or {}).get(('peto' if method=='PETO' else 'mh')+'_p')
            d=math.inf if a is None or not math.isfinite(a) else abs(a-b)/b if b>0 else 0 if a==0 else math.inf
            rows.append(dict(configuration=app['id'],quantity=method+'.p',app=a,reference=b,z=ref.get('zval'),difference=d if math.isfinite(d) else None,passed=d<=1e-9))
    return dict(checks=len(rows),passed=sum(r['passed'] for r in rows),z_ge_8=sum(abs(r['z'])>=8 for r in rows),tolerance=1e-9,rows=rows)
