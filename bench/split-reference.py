from pathlib import Path
import shutil
p=Path('build.R');s=p.read_text(encoding='utf8')
cut=s.index('refs<-list();warnings<-list()')
serializer=s[s.index('# JSON writer'):s.index("items<-unique(data(package='metadat')")]
ref=s[cut:]
ref=ref.replace('z<-cfg$rows;id<-', "z<-cfg$rows;for(col in c('ai','bi','ci','di'))z[[col]]<-as.numeric(z[[col]]);id<-")
ref=ref.replace("sum(vapply(audit,function(x)x$configurations>0,TRUE))", "length(unique(vapply(corpus,function(x)x$dataset,'')))")
Path('reference.R').write_text("library(metafor)\nlibrary(metadat)\n"+serializer+"corpus<-readRDS('corpus.rds')\nitems<-unique(data(package='metadat')$results[,'Item'])\n"+ref,encoding='utf8')
p.write_text(s[:cut]+"source('reference.R')\n",encoding='utf8')
shutil.copyfile('reference.json','reference-integer-overflow.json')
print('Reference uses unchanged count values stored as R doubles; prior integer-overflow evidence retained')
