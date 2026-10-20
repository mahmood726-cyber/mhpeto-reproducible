# Check the native reference environment before a costly replay.
userlibs <- strsplit(Sys.getenv('R_LIBS_USER'), .Platform$path.sep, fixed=TRUE)[[1]]
.libPaths(c(userlibs[nzchar(userlibs)], .libPaths()))
print(.libPaths())
print(R.version.string)
for (p in c('metafor','meta','jsonlite')) {
  if (!requireNamespace(p, quietly=TRUE)) stop('Missing package: ',p)
  cat(p, as.character(packageVersion(p)), '\n')
}
stopifnot(packageVersion('metafor') == package_version('5.2-1'),
          packageVersion('meta') == package_version('8.5-0'))
cat('R PACKAGE VERSIONS PASS\n')
