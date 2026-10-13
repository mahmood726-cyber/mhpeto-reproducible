library(metadat)
items <- unique(data(package='metadat')$results[,'Item'])
dir.create('dataset-docs',showWarnings=FALSE)
for(nm in items) {
 h<-help(nm,package='metadat')
 if(length(h)) writeLines(capture.output(tools::Rd2txt(utils:::.getHelpFile(h))),paste0('dataset-docs/',nm,'.txt'))
}
