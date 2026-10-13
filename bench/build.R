library(metadat)
library(metafor)
options(warn=1)
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
items<-unique(data(package='metadat')$results[,'Item']); corpus<-list();audit<-list(); excluded.rows<-list()
add<-function(nm,x,outcome,cols,mode='total',group=NULL) {
 stopifnot(all(cols %in% names(x)))
 a<-x[[cols[1]]]; b<-x[[cols[2]]]; c<-x[[cols[3]]];d<-x[[cols[4]]]
 if(mode=='total'){b<-b-a;d<-d-c}
 z<-data.frame(source_row=x$.row,ai=a,bi=b,ci=c,di=d)
 good<-complete.cases(z)&apply(z[,2:5],1,function(v) all(is.finite(v)&v>=0&v==floor(v)))&(a+b>0)&(c+d>0)
 good[is.na(good)]<-FALSE
 if(any(!good)) excluded.rows[[length(excluded.rows)+1]]<<-list(dataset=nm,outcome=outcome,rows=x$.row[!good],reason='Missing, noninteger, negative cells or nonpositive arm size')
 z<-z[good,,drop=FALSE];g<-if(is.null(group)) rep('all',nrow(x)) else apply(x[,group,drop=FALSE],1,paste,collapse=' / ');g<-g[good]
 for(gr in unique(g)) {
  zz<-z[g==gr,,drop=FALSE]; id<-paste(nm,outcome,gr,sep='|')
  corpus[[length(corpus)+1]]<<-list(id=id,dataset=nm,outcome=outcome,comparison=gr,mapping=paste(cols,collapse=','),mode=mode,rows=zz)
 }
}
arm<-function(nm,x,event,total,trt,study,outcome=event){
 stopifnot(all(c(event,total,trt,study) %in% names(x)))
 lev<-sort(unique(as.character(x[[trt]])));if(length(lev)<2)return()
 for(pair in combn(lev,2,simplify=FALSE)){
  l<-x[as.character(x[[trt]])==pair[1],,drop=FALSE];r<-x[as.character(x[[trt]])==pair[2],,drop=FALSE]
  # Combine duplicate arms of the same treatment within a study, retaining source row IDs.
  ag<-function(d){ss<-split(d,as.character(d[[study]]));do.call(rbind,lapply(names(ss),function(s){v<-ss[[s]];data.frame(study=s,e=sum(v[[event]]),n=sum(v[[total]]),row=paste(v$.row,collapse='+'))}))}
  if(!nrow(l)||!nrow(r)) next
  q<-merge(ag(l),ag(r),by='study',suffixes=c('1','2'));if(!nrow(q))next
  q$.row<-paste(q$row1,q$row2,sep='/');q$comparison<-paste(pair,collapse=' vs ')
  add(nm,q,outcome,c('e1','n1','e2','n2'),group='comparison')
 }
}
for(nm in items){
 e<-new.env();data(list=nm,package='metadat',envir=e);x<-e[[nm]];before<-length(corpus)
 if(is.data.frame(x)) {
 x$.row<-seq_len(nrow(x)); nn<-names(x)
 if(all(c('ai','bi','ci','di')%in%nn)) add(nm,x,'binary',c('ai','bi','ci','di'),'cells')
 else if(all(c('ai','n1i','ci','n2i')%in%nn)) add(nm,x,'binary',c('ai','n1i','ci','n2i'),group=if(nm=='dat.yusuf1985') 'table' else if(nm=='dat.linde2005') 'group' else NULL)
 else if(all(c('Ee','Ne','Ec','Nc')%in%nn)) add(nm,x,'binary',c('Ee','Ne','Ec','Nc'))
 else if(all(c('tpos','tneg','cpos','cneg')%in%nn)) add(nm,x,'tuberculosis',c('tpos','tneg','cpos','cneg'),'cells')
 if(nm=='dat.axfors2021')add(nm,x,'death',c('hcq_arm_event','hcq_arm_total','control_arm_event','control_arm_total'),group=c('hcq_cq','Control'))
 if(nm=='dat.bornmann2007')add(nm,x,'award',c('waward','wtotal','maward','mtotal'))
 if(nm=='dat.bourassa1996')add(nm,x,'left-eye vs right-eye',c('lh.le','rh.le','lh.re','rh.re'),'cells')
 if(nm=='dat.cannon2006')for(i in 1:6)add(nm,x,paste0('ep',i),c(paste0('ep',i,'t'),'nt',paste0('ep',i,'c'),'nc'))
 if(nm=='dat.chiarito2020')for(o in c('mi','stroke','death','vdeath'))add(nm,x,o,c(paste0('p2y12.',o),'p2y12.total',paste0('aspirin.',o),'aspirin.total'))
 if(nm=='dat.collins1985a')for(o in c('b','o','d'))add(nm,x,o,c(paste0(o,'.xti'),'nti',paste0(o,'.xci'),'nci'),group=c('trt','ctrl'))
 if(nm=='dat.collins1985b')for(o in c('pre','ped','stb','ned'))add(nm,x,o,c(paste0(o,'.xti'),if(o=='pre')'pre.nti' else 'fup.nti',paste0(o,'.xci'),if(o=='pre')'pre.nci' else 'fup.nci'))
 if(nm=='dat.dagostino1998')add(nm,x,'binary',c('xt','nt','xc','nc'),group=c('outcome','drug'))
 if(nm=='dat.damico2009')add(nm,x,'binary',c('xt','nt','xc','nc'))
 if(nm=='dat.dorn2007')add(nm,x,'binary',c('x.a','n.a','x.p','n.p'))
 if(nm=='dat.fine1993')for(i in 1:4)add(nm,x,paste0('survival',i),c(paste0('e',i,'i'),'nei',paste0('c',i,'i'),'nci'))
 if(nm=='dat.frank2008') {x$bc.other<-x$bc.ins.del+x$bc.del.del;x$ct.other<-x$ct.ins.del+x$ct.del.del;add(nm,x,'ins.ins vs other genotype',c('bc.ins.ins','bc.other','ct.ins.ins','ct.other'),'cells')}
 if(nm=='dat.hartmannboyce2018')add(nm,x,'cessation',c('x.nrt','n.nrt','x.ctrl','n.ctrl'),group='treatment')
 if(nm=='dat.higgins2008')add(nm,x,'observed response',c('resp.halo','fail.halo','resp.plac','fail.plac'),'cells')
 if(nm=='dat.hart1999')add(nm,x,'stroke counts over patients (not person-time)',c('x1i','n1i','x2i','n2i'),group='compgrp')
 if(nm=='dat.kearon1998'){x$fp<-x$nn-x$tn;add(nm,x,'test positive in cases vs noncases',c('tp','np','fp','nn'),group='patients')}
 if(nm=='dat.rivera2025')add(nm,x,'test positive in cases vs noncases',c('TP','FN','FP','TN'),'cells')
 if(nm=='dat.karner2014')for(o in c('exa','sexa','hospi','deaths','sae','dropout'))add(nm,x,o,c(paste0('tiotropium.',o),'tiotropium.total',paste0('placebo.',o),'placebo.total'))
 if(nm=='dat.landenberger2005')add(nm,x,'recidivism',c('n.cbt.rec','n.cbt.non','n.ctrl.rec','n.ctrl.non'),'cells')
 if(nm=='dat.nissen2007')for(o in c('infarction','death'))add(nm,x,o,c(paste0('treat.',o),'treat.total',paste0('cont.',o),'cont.total'))
 if(nm=='dat.obrien2003')arm(nm,x,'cases','total','grp','study','preeclampsia by within-study BMI category rank')
 if(nm%in%c('dat.roever2022','dat.ursino2021'))arm(nm,x,'events','total','dose','study','dose-limiting toxicity by dose cohort')
 if(nm=='dat.thompson1999')add(nm,x,'IHD',c('ihd.exp','noihd.exp','ihd.cont','noihd.cont'),'cells')
 if(nm=='dat.vanhowe1999')add(nm,x,'positive',c('cir.pos','cir.neg','non.pos','non.neg'),'cells')
 if(nm=='dat.viechtbauer2021')add(nm,x,'binary',c('xTi','nTi','xCi','nCi'))
 specs<-list(dat.baker2009=c('exac','total','treatment','study'),dat.dogliotti2014=c('stroke','total','treatment','study'),dat.dong2013=c('death','randomized','treatment','id'),dat.gurusamy2011=c('death','n','treatment','study'),dat.hasselblad1998=c('xi','ni','trt','study'),dat.linde2016=c('resp','n','int','id'),dat.pagliaro1992=c('xi','ni','trt','study'),dat.woods2010=c('r','N','treatment','author'))
 if(nm%in%names(specs)){s<-specs[[nm]];arm(nm,x,s[1],s[2],s[3],s[4])}
 if(nm=='dat.tian2009')for(o in c('deaths','infarcts'))arm(nm,x,o,'n','group','study')
 if(nm=='dat.linde2015')for(o in c('resp','remi','loss','loss.ae','ae')){
  z<-do.call(rbind,lapply(1:3,function(i)data.frame(id=x$id,treatment=x[[paste0('treatment',i)]],e=x[[paste0(o,i)]],n=x[[paste0('n',i)]],.row=paste0(x$.row,':arm',i))));z<-z[!is.na(z$treatment),];arm(nm,z,'e','n','treatment','id',o)
 }
 }
 used<-length(corpus)-before
 reason<-if(used) 'Documented binary counts; mappings and source rows in corpus.json' else 'No documented two-group binary count structure; see inventory and package documentation'
 if(nm=='dat.hart1999')reason<-'Structural counts over patient denominators; validates numerical 2x2 calculation, not original person-time incidence-rate analysis'
 if(nm%in%c('dat.kearon1998','dat.rivera2025'))reason<-'Structural diagnostic 2x2 tables; cases versus noncases as groups, test positivity as outcome; not a treatment-effect interpretation'
 if(nm%in%c('dat.roever2022','dat.ursino2021'))reason<-'Within-study dose cohort pairs; numerical 2x2 validation only, not randomized concurrent treatment contrasts'
 audit[[length(audit)+1]]<-list(dataset=nm,configurations=used,reason=reason,columns=names(x))
}
writeLines(js(corpus),'corpus.json',useBytes=TRUE);writeLines(js(audit),'dataset-audit.json',useBytes=TRUE);writeLines(js(excluded.rows),'excluded-rows.json',useBytes=TRUE)
saveRDS(corpus,'corpus.rds')
source('reference.R')
