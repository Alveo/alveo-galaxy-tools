#
# Galaxy tool that plots Vowels using the phonR package.
# Accepts 8 inputs of the form <tsv data file> <output file name> <column1> <column2> <optPretty> <optEllipse> <optTokens> <optMeans>
# Created by Michael Bauer
#
library(phonR)
library('getopt')

#create options
option_specification = matrix(c(
  'outdir', 'f', 1, 'character',
  'htmlfile', 'h', 1, 'character',
  'inputfile', 'i', 1, 'character',
  'column1', 'y', 1, 'integer',
  'column2', 'z', 1, 'integer',
  'columnvowels', 'x', 1, 'integer',
  'pretty', 'p', 1, 'logical',
  'ellipse', 'e', 1, 'logical',
  'tokens', 't', 1, 'logical',
  'means', 'm', 1, 'logical',
  'cextokens', 'c', 1, 'numeric',
  'alphatokens', 'a', 1, 'numeric',
  'cexmeans', 'b', 1, 'numeric'
), byrow=TRUE, ncol=4);

# Parse options
options = getopt(option_specification);

if (!is.null(options$outdir)) {
  # Create the directory
  dir.create(options$outdir,FALSE)
}

pngfile <- gsub("[ ]+", "", paste(options$outdir,"/pngfile.png"))
htmlfile <- gsub("[ ]+", "", paste(options$htmlfile))

data = read.table(options$inputfile,sep="\t", header=TRUE);

png(pngfile);

plotVowels(data[,options$column1], data[,options$column2], data[,options$columnvowels], plot.tokens = options$tokens, 
          pch.tokens = data[,options$columnvowels], cex.tokens = options$cextokens, alpha.tokens = options$alphatokens, 
          plot.means = options$means, pch.means = data[,options$columnvowels], cex.means = options$cexmeans, 
          var.col.by = data[,options$columnvowels], ellipse.line = options$ellipse, pretty = options$pretty)
dev.off();

htmlfile_handle <- file(htmlfile)
html_output = c('<html><body>',
                '<h3>Result:</h3><img src="pngfile.png"/>',
                '</html></body>');
writeLines(html_output, htmlfile_handle);
close(htmlfile_handle);
