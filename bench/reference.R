library(metafor)
library(metadat)
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
corpus<-readRDS('corpus.rds')
items<-unique(data(package='metadat')$results[,'Item'])
refs<-list();warnings<-list()
for(cfg in corpus)for(m in c('OR','RR','RD','PETO')){
 z<-cfg$rows;for(col in c('ai','bi','ci','di'))z[[col]]<-as.numeric(z[[col]]);id<-paste(cfg$id,m,sep='|');ws<-character()
 fit<-tryCatch(withCallingHandlers(if(m=='PETO')rma.peto(ai=z$ai,bi=z$bi,ci=z$ci,di=z$di,add=0,to='none',drop00=TRUE) else rma.mh(ai=z$ai,bi=z$bi,ci=z$ci,di=z$di,measure=m,add=c(.5,0),to=c('only0','none'),drop00=c(FALSE,FALSE),correct=FALSE),warning=function(w){ws<<-c(ws,conditionMessage(w));invokeRestart('muffleWarning')}),error=function(e)e)
 rr<-list(id=id,k_input=nrow(z),warnings=as.list(ws))
 if(inherits(fit,'error'))rr$error<-conditionMessage(fit) else {
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
writeLines(js(refs),'reference.json',useBytes=TRUE)
writeLines(capture.output(sessionInfo()),'session.txt')
cat(sprintf('Enumerated %d datasets; used %d; configurations %d; reference fits %d\n',length(items),length(unique(vapply(corpus,function(x)x$dataset,''))),length(corpus),length(refs)))
