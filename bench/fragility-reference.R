library(metafor)
corpus<-readRDS('corpus.rds')
Z<-qnorm(.975)
# Independent R DL implementation for the greedy search; each initial and final
# model is also checked against metafor::rma.uni below.
pool<-compiler::cmpfun(function(z,m){
 keep<-!((z[,1]==0&z[,3]==0)|(z[,2]==0&z[,4]==0));z<-z[keep,,drop=FALSE]
 if(!nrow(z))return(rep(NA_real_,3))
 zero<-apply(z==0,1,any);z[zero,]<-z[zero,]+.5
 a<-z[,1];b<-z[,2];c<-z[,3];d<-z[,4];n1<-a+b;n2<-c+d
 if(m=='OR'){y<-log(a*d/(b*c));v<-1/a+1/b+1/c+1/d}
 if(m=='RR'){y<-log((a/n1)/(c/n2));v<-1/a-1/n1+1/c-1/n2}
 if(m=='RD'){y<-a/n1-c/n2;v<-a*b/n1^3+c*d/n2^3}
 w<-1/v;mu<-sum(w*y)/sum(w);q<-sum(w*(y-mu)^2);den<-sum(w)-sum(w^2)/sum(w)
 tau<-if(length(y)>1)max(0,(q-length(y)+1)/den) else 0
 w<-1/(v+tau);mu<-sum(w*y)/sum(w);se<-sqrt(1/sum(w));c(mu,mu-Z*se,mu+Z*se)
})
metapool<-function(z,m){
 f<-suppressWarnings(tryCatch(rma.uni(measure=m,ai=z[,1],bi=z[,2],ci=z[,3],di=z[,4],add=.5,to='only0',drop00=TRUE,method='DL'),error=function(e)NULL))
 if(is.null(f))return(rep(NA_real_,3));c(as.numeric(f$beta),f$ci.lb,f$ci.ub)
}
num<-function(x)ifelse(is.finite(x),sprintf('%.17g',x),'null')
out<-list();n<-0;done<-character()
if(file.exists('fragility-reference.json')&&file.exists('corpus-prior.rds')){
 oldcorpus<-readRDS('corpus-prior.rds');cur<-setNames(corpus,vapply(corpus,function(c)c$id,''))
 for(c in oldcorpus)stopifnot(identical(c,cur[[c$id]]))
 txt<-paste(readLines('fragility-reference.json'),collapse='')
 out<-as.list(strsplit(substring(txt,2,nchar(txt)-1),'(?<=\\}),(?=\\{)',perl=TRUE)[[1]])
 done<-vapply(out,function(s)sub('^.*?"id":"([^"]+)".*$','\\1',s),'')
 n<-length(out)
}
for(cfg in corpus)for(m in c('OR','RR','RD')){
 if(nrow(cfg$rows)<2)next
 if(paste(cfg$id,m,sep='|')%in%done)next
 z<-as.matrix(cfg$rows[,c('ai','bi','ci','di')]);total<-sum(z);ori<-pool(z,m);baseline<-metapool(z,m)
 if(any(is.finite(ori)!=is.finite(baseline)) || any(abs(ori-baseline)>1e-9,na.rm=TRUE))stop('Independent DL baseline differs from metafor')
 sig<-is.finite(ori[2])&&(ori[3]<0||ori[2]>0);fi<-NA_real_;last<-ori;less<-ori[3]<0;steps<-0
 if(sig)while(sig&&steps<100000){
  best<-NULL;boundbest<-if(less)-Inf else Inf;flipbest<-FALSE
  for(i in seq_len(nrow(z))){
   for(arm in c(0,1)){
    if(arm==0){if((less&&z[i,3]<=0)||(!less&&z[i,4]<=0))next;delta<-if(less)-1 else 1;cols<-c(3,4)}
    else{if((less&&z[i,2]<=0)||(!less&&z[i,1]<=0))next;delta<-if(less)1 else -1;cols<-c(1,2)}
    zz<-z;zz[i,cols]<-zz[i,cols]+c(delta,-delta);f<-pool(zz,m)
    bnd<-if(less)f[3] else f[2];if(!is.finite(bnd))next
    flip<-if(less)bnd>=0 else bnd<=0
    if(is.null(best)||(if(less)bnd>boundbest else bnd<boundbest)){best<-zz;boundbest<-bnd;flipbest<-flip;last<-f}
    if(flip){best<-zz;flipbest<-TRUE;last<-f;break}
   }
   if(flipbest)break
  }
  if(is.null(best))break
  z<-best;steps<-steps+1;sig<-!flipbest
  if(!sig)fi<-steps
 }
 final<-metapool(z,m)
 if(any(abs(last-final)>1e-9,na.rm=TRUE))stop('Final DL fit differs from metafor')
 id<-paste(cfg$id,m,sep='|')
 out[[length(out)+1]]<-paste0('{"id":',encodeString(id,quote='"'),',"FI":',num(fi),',"FQ":',num(fi/total),',"beta":',num(baseline[1]),',"lo":',num(baseline[2]),',"hi":',num(baseline[3]),',"final_lo":',num(final[2]),',"final_hi":',num(final[3]),'}')
 n<-n+1;if(n%%30==0)cat('Fragility configurations:',n,'\n')
 writeLines(paste0('[',paste(out,collapse=','),']'),'fragility-reference.json')
}
cat(sprintf('Validated %d greedy DL fragility configurations; initial and final fits agree with metafor at 1e-9\n',n))
