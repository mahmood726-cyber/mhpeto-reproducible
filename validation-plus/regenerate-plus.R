# Optional regeneration in scratch; never overwrite pinned reference JSON.
userlibs <- strsplit(Sys.getenv('R_LIBS_USER'), .Platform$path.sep, fixed=TRUE)[[1]]
.libPaths(c(userlibs[nzchar(userlibs)], .libPaths()))
source('analysis/check-r-versions.R')
root <- normalizePath('.', winslash='/')
dest <- file.path(root,'rerun/plus-oracle')
if (dir.exists(dest)) stop('Move rerun/plus-oracle before regenerating')
dir.create(file.path(dest,'validate','corpus'),recursive=TRUE)
dir.create(file.path(dest,'validate','plus-corpus'),recursive=TRUE)
stopifnot(file.copy('validation-plus/corpus/corpus.json',file.path(dest,'validate','corpus','corpus.json')))
setwd(dest)
source(file.path(root,'validation-plus','generate-plus.R'),chdir=FALSE)
cat('Fresh R oracle written under rerun/plus-oracle; pinned archive inputs unchanged.\n')
