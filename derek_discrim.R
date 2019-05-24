require(mgc)
require(igraph)
require(stringr)
require(fmriutils)
require(reshape2)
require(ggplot2)

fmriu.list2array <- function(list_in, flatten=FALSE) {
  nroi <- max(sapply(list_in, function(graph) dim(graph)[1]))
  nsub <- length(list_in)
  array_out <- array(NaN, dim=c(nsub, nroi, nroi))
  subnames <- names(list_in)
  incl_ar <- logical(nsub)
  for (i in 1:nsub) {
    if (isTRUE(all.equal(dim(list_in[[i]]), c(nroi, nroi)))) {
      array_out[i,,] <-list_in[[i]]
      incl_ar[i] <- TRUE
    }
  }
  array_out <- array_out[incl_ar,,]
  subnames <- subnames[incl_ar]
  if (flatten) {
    dimar <- dim(array_out)
    if (!is.na(dimar[3])){
      dim(array_out) <- c(dimar[1], dimar[2]*dimar[3])
    }
  }
  return(list(array=array_out, incl_ar=incl_ar, names=subnames))
}

fmriu.io.open_graphs <- function(ipath, dataset_id="", atlas_id="",
                                 fmt='elist', verbose=FALSE, rtype='list', flatten=FALSE,
                                 rem.diag=TRUE) {
  if (! (fmt %in% c('adj', 'elist'))) {
    stop('You have passed an invalid format type. Options are: [\'adj\', \'elist\', and \'graphml\'].')
  }
  
  if (fmt == 'elist') {
    fmt = 'ncol'; ext = "ssv"
  } else if (fmt == "graphml") {
    fmt = "graphml"; ext = "graphml"
  } else if (fmt == "adj") {
    fmt = "adj"; ext="adj"
  }
  
  fnames <- paste(ipath, list.files(ipath, pattern = atlas_id), sep='/')
  if (! (rtype %in% c('list', 'array'))) {
    stop('You have passed an invalid return type. Options are: [\'list\', \'array\'].')
  }
  
  print(sprintf("opening graphs for %s dataset and %s parcellation atlas...", dataset_id, atlas_id))
  subjects <- vector("character", length(fnames))
  sessions <- vector("character", length(fnames))
  tasks <- vector("character", length(fnames))
  gr <- list()
  
  vertices <- c()
  
  # so that we don't get any annoying errors if particular vertices are empty
  if (fmt != "adj") {
    for (i in 1:length(fnames)) {
      tgr <- igraph::read_graph(fnames[i], format=fmt) # read the graph from the filename
      vertices <- union(vertices, V(tgr)$name)
    }
  }
  
  vertices <- vertices[ordered(as.numeric(vertices))]
  counter <- 1
  for (i in 1:length(fnames)) {
    basename <- basename(fnames[i])     # the base name of the file
    if (verbose) {
      print(paste('Loading', basename, '...'))
    }
    igr <- tryCatch({
      igraph::read_graph(fnames[i], format=fmt, predef=vertices) # read the graph from the filename, ordering by the vertices we found previously
    }, error = function(e) {
      return(NaN)
    })
    
    if (is.igraph(igr)) {
      tgr <- get.adjacency(igr, type="both", attr="weight", sparse=FALSE) # convert graph to adjacency matrix
      tgr[is.nan(tgr)] <- 0  # missing entries substituted with 0s
      if (rem.diag) {
        diag(tgr) <- 0
      }
      colnames(tgr) <- V(igr); rownames(tgr) <- V(igr)
      gr[[basename]] <-t(tgr)
      subjects[counter] <- str_extract(basename, 'sub(.?)+?(?=_)')
      sessions[counter] <- str_extract(basename, 'ses(.?)+?(?=_)')
      tasks[counter] <- str_extract(basename, 'task(.?)+?(?=_)')
      counter <- counter + 1
    }
  }
  
  dataset <- rep(dataset_id, counter - 1)
  atlas <- rep(atlas_id, counter - 1)
  subjects <- subjects[1:counter - 1]
  sessions <- sessions[1:counter - 1]
  tasks <- tasks[1:counter - 1]
  
  if (rtype == 'array') {
    aro <- fmriu.list2array(gr, flatten=flatten)
    gr <- aro$array
    dataset <- dataset[aro$incl_ar]
    atlas <- atlas[aro$incl_ar]
    subjects <- subjects[aro$incl_ar]
    sessions <- sessions[aro$incl_ar]
    tasks <- tasks[aro$incl_ar]
  }
  return(list(graphs=gr, dataset=dataset, atlas=atlas, subjects=subjects,
              sessions=sessions, tasks=tasks))
}

studies <- c('BNU1', 'HNU1', 'KKI', 'NKI', 'SWU')
# studies <- c('NKI')

atlases <- c("desikan")

df <- setNames(data.frame(matrix(ncol = length(studies), nrow = length(atlases))), studies)
row.names(df) <- atlases

for (study in studies) {
  ipath <- paste("/Users/alex/Dropbox/NeuroData/ndmg-paper/data/native_graphs_", study, sep="")
  print(study)
  for (atlas in atlases) {
    print(atlas)
    inputs <- try(fmriu.io.open_graphs(ipath, fmt="elist", rtype="array", dataset_id=study, atlas_id=atlas, flatten=TRUE, rem.diag=TRUE))
    res <- try(discr.stat(inputs$graphs, inputs$subjects))
    print(res)
    try(df[atlas, study] <- res)
    remove(inputs)
  }
}