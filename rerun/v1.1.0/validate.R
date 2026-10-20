# Standalone offline validation; no Python, browser or downloads required.
main <- function() {
 # Prefer the explicitly selected user library; R_LIBS may contain older packages.
 userlibs <- strsplit(Sys.getenv('R_LIBS_USER'),.Platform$path.sep,fixed=TRUE)[[1]]
 .libPaths(c(userlibs[nzchar(userlibs)],.libPaths()))
 for(pkg in c('metafor','jsonlite'))if(!requireNamespace(pkg,quietly=TRUE))stop('Missing installed package: ',pkg)
 library(metafor)
 cat(R.version.string,'\nmetafor ',as.character(packageVersion('metafor')),'; paper 5.2-1\n',sep='')
 cat('Recomputed: every MH/Peto fit, study effect and inverse-variance Labbe reference.\n')
 cat('Replayed: archived browser numerical outputs, rounded UI and structural evidence; independent R greedy FI/FQ and DL baseline oracle records. No browser or greedy search is run.\n')
# JSON writer: finite numeric values at 17 significant digits; missing/nonfinite -> null.
js <- function(x) {
 if(is.null(x)) return('null')
 if(is.data.frame(x)) return(paste0('[',paste(vapply(seq_len(nrow(x)),function(i) js(as.list(x[i,,drop=FALSE])),''),collapse=','),']'))
 if(is.list(x)) {v<-vapply(x,js,'');if(!is.null(names(x))) return(paste0('{',paste(paste0(vapply(names(x),js,''),':',v),collapse=','),'}'));return(paste0('[',paste(v,collapse=','),']'))}
 if(length(x)!=1) return(js(as.list(x)))
 if(is.na(x)) return('null')
 if(is.numeric(x)) return(if(is.finite(x)) sprintf('%.17g',x) else 'null')
 if(is.logical(x)) return(if(x) 'true' else 'false')
 encodeString(as.character(x),quote='"')
}
corpus<-jsonlite::fromJSON('data/corpus.json',simplifyVector=FALSE)
 # Validate keys before setNames can conceal multiplicity or missing fields.
 index<-function(xs,expected=NULL,key='id') {
   if(!is.list(xs))stop('Invalid record collection')
   ids<-vapply(xs,function(x){
     if(!is.list(x)||anyDuplicated(names(x))||!key%in%names(x)||
        !is.character(x[[key]])||length(x[[key]])!=1L||!nzchar(x[[key]]))stop('Invalid record key: ',key)
     x[[key]]
   },'')
   if(anyDuplicated(ids))stop('Duplicate record identifiers: ',key)
   if(!is.null(expected)&&(length(ids)!=length(expected)||!setequal(ids,expected)))stop('Record cardinality/identifier mismatch: ',key)
   setNames(xs,ids)
 }
 index(corpus)
 scalar<-function(x) is.null(x)||identical(x,NA)||(is.numeric(x)&&length(x)==1L&&!is.nan(x)&&(is.na(x)||is.finite(x)))
 fields<-function(x,keys,where,nullable=TRUE) {
   if(!is.list(x)||anyDuplicated(names(x))||!all(keys%in%names(x)))stop('Missing/invalid evidence: ',where)
   for(k in keys)if(!scalar(x[[k]])||(!nullable&&(!is.numeric(x[[k]])||length(x[[k]])!=1L||!is.finite(x[[k]]))))stop('Invalid evidence: ',where,'.',k)
 }
 for(cfg in corpus) {
   if(!is.list(cfg$rows)||!length(cfg$rows))stop('Invalid source rows: ',cfg$id)
   for(row in cfg$rows) {
     fields(row,c('ai','bi','ci','di'),cfg$id,FALSE)
     if(!'source_row'%in%names(row)||length(row$source_row)!=1L||!(is.character(row$source_row)||is.numeric(row$source_row))||is.na(row$source_row)||!nzchar(as.character(row$source_row)))stop('Invalid source row key: ',cfg$id)
     v<-unlist(row[c('ai','bi','ci','di')])
     if(any(!is.finite(v))||any(v<0)||any(v!=floor(v))||row$ai+row$bi<=0||row$ci+row$di<=0)stop('Invalid source counts: ',cfg$id)
   }
   if(anyDuplicated(vapply(cfg$rows,function(r)as.character(r$source_row),'')))stop('Duplicate source rows: ',cfg$id)
 }
corpus<-lapply(corpus,function(cfg){cfg$rows<-do.call(rbind,lapply(cfg$rows,as.data.frame));cfg})

refs<-list();warnings<-list()
for(cfg in corpus)for(m in c('OR','RR','RD','PETO')){
 z<-cfg$rows;for(col in c('ai','bi','ci','di'))z[[col]]<-as.numeric(z[[col]]);id<-paste(cfg$id,m,sep='|');ws<-character()
 fit<-tryCatch(withCallingHandlers(if(m=='PETO')rma.peto(ai=z$ai,bi=z$bi,ci=z$ci,di=z$di,add=0,to='none',drop00=TRUE) else rma.mh(ai=z$ai,bi=z$bi,ci=z$ci,di=z$di,measure=m,add=c(.5,0),to=c('only0','none'),drop00=c(FALSE,FALSE),correct=FALSE),warning=function(w){ws<<-c(ws,conditionMessage(w));invokeRestart('muffleWarning')}),error=function(e)e)
 rr<-list(id=id,k_input=nrow(z),warnings=as.list(ws))
 if(inherits(fit,'error')) {
   rr$error<-conditionMessage(fit)
   # A caught R fit error explicitly declares these method results undefined.
   for(v in c('est','lo','hi','zval','pval','beta','se'))rr[v]<-list(NULL)
 } else {
 for(v in c('beta','se','ci.lb','ci.ub','zval','pval','MH','MHp','TA','TAp','BD','BDp','QE','QEp','I2','H2','k'))rr[[v]]<-if(is.null(fit[[v]]))NULL else as.numeric(fit[[v]])
 rr$est<-if(m=='RD')as.numeric(fit$beta) else exp(as.numeric(fit$beta));rr$lo<-if(m=='RD')fit$ci.lb else exp(fit$ci.lb);rr$hi<-if(m=='RD')fit$ci.ub else exp(fit$ci.ub)
 }
 if(m!='PETO'){
 es<-suppressWarnings(escalc(measure=m,ai=z$ai,bi=z$bi,ci=z$ci,di=z$di,add=if(m=='RD')0 else .5,to='only0',drop00=FALSE))
 rr$studies<-lapply(seq_len(nrow(z)),function(i){b<-es$yi[i];se<-sqrt(es$vi[i]);tr<-if(m=='RD')identity else exp;list(beta=b,se=se,est=tr(b),lo=tr(b-qnorm(.975)*se),hi=tr(b+qnorm(.975)*se))})
 # Diagnostic uses IV FE OR when the selected measure is RD (page's shipped behavior).
 lm<-if(m=='RR')'RR' else 'OR';ee<-suppressWarnings(escalc(measure=lm,ai=z$ai,bi=z$bi,ci=z$ci,di=z$di,add=.5,to='only0',drop00=FALSE))
 lf<-rma.uni(ee$yi,ee$vi,method='FE');rr$labbe<-list(logEff=as.numeric(lf$beta),eff=exp(as.numeric(lf$beta)),pc=z$ci/(z$ci+z$di),pt=z$ai/(z$ai+z$bi))
 }
 refs[[length(refs)+1]]<-rr
}

 apps<-jsonlite::fromJSON('results/app-patched.json',simplifyVector=FALSE)
 frag<-jsonlite::fromJSON('results/fragility-reference.json',simplifyVector=FALSE)
 cc<-index(corpus)
 rr<-index(refs,unlist(lapply(names(cc),function(id)paste(id,c('OR','RR','RD','PETO'),sep='|'))))
 expected<-unlist(lapply(names(cc),function(id)paste(id,c('OR','RR','RD'),sep='|')))
 index(apps,expected)
 eligible<-unlist(lapply(corpus,function(c)if(nrow(c$rows)>=2)paste(c$id,c('OR','RR','RD'),sep='|')else character()))
 ff<-index(frag,eligible)
 for(r in refs)if(r$k_input>=2)fields(r,c('est','lo','hi','zval','pval','beta','se'),r$id)
 for(f in frag)fields(f,c('FI','FQ','beta','lo','hi'),f$id)
 # Match diagnostic-plots.js: 0.001 + repeated 0.01 steps, clipped to pt <= 1.
 curve_shape<-function(lb,m,id) {
   grid<-numeric();pc<-0.001;eff<-exp(lb[['logEff',exact=TRUE]])
   while(pc<=0.999) {
     pt<-if(m=='RR')eff*pc else (pc/(1-pc)*eff)/(1+pc/(1-pc)*eff)
     if(is.finite(pt)&&pt>=0&&pt<=1)grid<-c(grid,pc)
     pc<-pc+0.01
   }
   # Exact key required: R's $ partially matches names (a renamed 'curve_backup' would be read as 'curve').
  if(!'curve'%in%names(lb))stop('Missing Labbe curve key: ',id)
  if(!is.list(lb[['curve',exact=TRUE]])||!length(lb[['curve',exact=TRUE]])||length(lb[['curve',exact=TRUE]])!=length(grid))stop('Invalid Labbe curve shape: ',id)
   for(i in seq_along(grid)) {
     fields(lb[['curve',exact=TRUE]][[i]],c('pc','pt'),id,FALSE)
     if(abs(lb[['curve',exact=TRUE]][[i]]$pc-grid[i])>1e-15)stop('Invalid Labbe curve grid: ',id)
   }
 }
 for(a in apps) {
   if(!all(c('result','studies','labbe','frag','pooledText','studyText')%in%names(a)))stop('Missing app record fields: ',a$id)
   for(k in c('pooledText','studyText'))if(!is.character(a[[k]])||length(a[[k]])!=1L)stop('Invalid UI evidence: ',a$id)
   if(!a$id%in%eligible)next
   m<-sub('^.*\\|','',a$id)
   for(prefix in if(m=='OR')c('mh','peto')else'mh')fields(a$result,paste(prefix,c('est','lo','hi','z','p'),sep='_'),a$id)
   fields(a$frag,c('FI','FQ'),a$id)
   fields(a$frag$pooled,c('est','lo','hi'),a$id)
   for(s in a$studies)fields(s,c('est','se'),a$id,FALSE)
   if(!is.null(a$labbe)) {
     fields(a$labbe,'logEff',a$id,FALSE)
     curve_shape(a$labbe,m,a$id)
     for(p in c(a$labbe[['points',exact=TRUE]],a$labbe[['curve',exact=TRUE]]))fields(p,c('pc','pt'),a$id,FALSE)
   }
 }
 ledger<-list();tails<-list()
 num<-function(x)if(is.numeric(x)&&length(x)==1L&&is.finite(x))as.numeric(x) else NA_real_
 check<-function(id,q,a,b,tol=1e-9,absolute=FALSE,mode='recomputed R versus archived browser') {
   valid<-scalar(a)&&scalar(b)
   a<-num(a);b<-num(b)
   delta<-if(!valid)Inf else if(is.na(a)&&is.na(b))0 else if(is.na(a)||is.na(b))Inf else abs(a-b)/(if(absolute||endsWith(q,'.p'))1 else max(1,abs(b)))
   if(endsWith(q,'.p')&&!is.na(b)&&b>=0&&b<1e-12) {
     d<-if(is.na(a))Inf else if(b>0)abs(a-b)/b else if(a==0)0 else Inf
     tails[[length(tails)+1L]]<<-data.frame(configuration=id,quantity=q,App=a,R=b,Difference=d,Tolerance=1e-9,Result=if(d<=1e-9)'PASS'else'FAIL')
   }
   ledger[[length(ledger)+1L]]<<-data.frame(configuration=id,quantity=q,App=a,R=b,Difference=delta,Tolerance=tol,Result=if(delta<=tol)'PASS' else 'FAIL',Mode=mode)
 }
 values<-function(s)as.numeric(regmatches(s,gregexpr('-?\\d+(?:\\.\\d+)?',s,perl=TRUE))[[1]])
 lines<-function(s)if(is.null(s)||!nzchar(s))character() else strsplit(s,'\n')[[1]]
 for(a in apps) {
   id<-a$id;m<-sub('^.*\\|','',id);base<-sub('\\|[^|]+$','',id);r<-rr[[id]];res<-a$result
   if(r$k_input<2) {
     check(id,paste0(m,'.single_row_refusal'),as.numeric(is.null(res)),1,mode='archived browser refusal')
     check(id,paste0(m,'.single_row_UI_clear'),as.numeric(!nzchar(a$pooledText)&&!nzchar(a$studyText)),1,mode='archived browser UI')
     next
   }
   for(method in if(m=='OR')c(m,'PETO')else m) {
     ref<-rr[[paste(base,method,sep='|')]];prefix<-if(method=='PETO')'peto'else'mh'
     for(q in c('est','lo','hi','z','p'))check(id,paste(method,q,sep='.'),res[[paste(prefix,q,sep='_')]],ref[[switch(q,z='zval',p='pval',q)]])
     est<-num(res[[paste0(prefix,'_est')]]);lo<-num(res[[paste0(prefix,'_lo')]]);hi<-num(res[[paste0(prefix,'_hi')]])
     beta<-if(m=='RD')est else if(!is.na(est)&&est>0)log(est)else NA_real_
     se<-if(!is.na(lo)&&!is.na(hi)&&(m=='RD'||(lo>0&&hi>0)))(if(m=='RD')hi-lo else log(hi)-log(lo))/(2*1.959963984540054)else NA_real_
     check(id,paste0(method,'.beta'),beta,ref$beta);check(id,paste0(method,'.se'),se,ref$se)
   }
   for(line in lines(a$pooledText)) {
     cells<-strsplit(line,'\t')[[1]];method<-if(cells[1]=='Peto OR')'PETO'else m;ref<-rr[[paste(base,method,sep='|')]]
     vv<-values(paste(cells[-1],collapse=' '))
     if(length(vv)==5L)for(j in seq_along(vv)) {
       q<-c('est','lo','hi','zval','pval')[j]
       check(id,paste0(method,'.display_pooled_',q),vv[j],ref[[q]],if(q=='zval').0050000001 else .0005000001,TRUE,'archived rounded UI versus recomputed R')
     }
   }
   rs<-r$studies;ss<-a$studies
   valid<-function(t)!is.na(num(t$se))&&num(t$se)>0&&!is.na(num(t$beta))
   check(id,paste0(m,'.study_count'),length(ss),sum(vapply(rs,valid,TRUE)))
   z<-cc[[base]]$rows
   bylabel<-index(ss,paste0('source-row-',z$source_row[vapply(rs,valid,TRUE)]),'label')
   for(i in seq_len(nrow(z))) {
     t<-rs[[i]];if(!valid(t))next
     st<-bylabel[[paste0('source-row-',z$source_row[i])]]
     check(paste0(id,'|row',i),paste0(m,'.study_beta'),st$est,t$beta)
     check(paste0(id,'|row',i),paste0(m,'.study_se'),st$se,t$se)
   }
   ll<-lines(a$studyText)
   for(i in seq_along(ll)) {
     cells<-strsplit(ll[i],'\t')[[1]];t<-rs[[i]];vv<-values(paste(cells[4:5],collapse=' '))
     if(length(vv)==3)for(j in 1:3){q<-c('est','lo','hi')[j];check(paste0(id,'|row',i),paste0(m,'.display_study_',q),vv[j],t[[q]],.0005000001,TRUE,'archived rounded UI versus recomputed R')}
     else check(paste0(id,'|row',i),paste0(m,'.display_study_defined'),length(vv),3,mode='archived UI structure')
   }
   lb<-a$labbe
   if(!is.null(lb)) {
     check(id,paste0(m,'.labbe_logEff'),lb[['logEff',exact=TRUE]],r$labbe[['logEff',exact=TRUE]])
     for(i in seq_along(lb[['points',exact=TRUE]]))for(q in c('pc','pt'))check(id,paste0(m,'.labbe_',q),lb[['points',exact=TRUE]][[i]][[q]],r$labbe[[q]][i])
     eff<-r$labbe$eff
     deltas<-vapply(lb[['curve',exact=TRUE]],function(p)abs(p$pt-(if(m=='RR')eff*p$pc else eff*p$pc/(1-p$pc+eff*p$pc))),0.)
     check(id,paste0(m,'.labbe_curve_max_abs_error'),max(c(0,deltas)),0)
   }
 }
 for(a in apps) {
   id<-a$id;if(!id%in%names(ff))next
   m<-sub('^.*\\|','',id);ref<-ff[[id]];f<-a$frag
   for(q in c('FI','FQ'))check(id,paste0(m,'.fragility_',q),f[[q]],ref[[q]],mode='replayed independent R greedy oracle versus archived browser')
   for(q in c('est','lo','hi')){rq<-if(q=='est')'beta'else q;check(id,paste0(m,'.fragility_DL_',rq),f$pooled[[q]],ref[[rq]],mode='replayed independent R DL baseline versus archived browser')}
 }
 result<-do.call(rbind,ledger)
 dir.create('outputs',showWarnings=FALSE)
 # write.csv normally serializes numeric values with only 15 significant digits.
 # Preserve the original doubles so the exported differences can be rechecked.
 exported<-result
 for(q in c('App','R','Difference','Tolerance'))exported[[q]]<-ifelse(is.na(result[[q]]),'NA',sprintf('%.17g',result[[q]]))
 write.csv(exported,'outputs/validate_R_table.csv',row.names=FALSE,na='NA')
 cat('\nPer-quantity totals:\n')
 for(q in sort(unique(result$quantity))) {
   z<-result[result$quantity==q,]
   cat(sprintf('%s: %d/%d pass; max difference %.17g; tolerance %g\n',q,sum(z$Result=='PASS'),nrow(z),max(z$Difference),z$Tolerance[1]))
 }
 passed<-sum(result$Result=='PASS');cat(sprintf('%d/%d checks pass\n',passed,nrow(result)))
 tailtable<-do.call(rbind,tails)
 exported<-tailtable
 for(q in c('App','R','Difference','Tolerance'))exported[[q]]<-ifelse(is.na(tailtable[[q]]),'NA',sprintf('%.17g',tailtable[[q]]))
 write.csv(exported,'outputs/validate_R_tails.csv',row.names=FALSE,na='NA')
 cat(sprintf('TAIL: %d/%d relative p-value checks pass; tolerance=1e-9\n',sum(tailtable$Result=='PASS'),nrow(tailtable)))
 if(nrow(result)!=68461L||passed!=68461L||!length(tails)||any(tailtable$Result!='PASS'))return(1L)
 0L
}
status<-tryCatch(main(),error=function(e){cat('Validation failed: ',conditionMessage(e),'\n',sep='',file=stderr());1L})
quit(save='no',status=status)
