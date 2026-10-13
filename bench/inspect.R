library(metadat)
library(metafor)
items <- unique(data(package='metadat')$results[,'Item'])
con <- file('inventory.txt','w')
for (nm in items) {e<-new.env();data(list=nm,package='metadat',envir=e); x<-e[[nm]];cat(nm,': ',paste(names(x),collapse=','),'\n',file=con)}
close(con)
writeLines(capture.output(metafor::rma.mh),'rma-mh-source.txt')
writeLines(capture.output(sessionInfo()),'session.txt')
