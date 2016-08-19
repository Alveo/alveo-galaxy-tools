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
  'column1', 'a', 1, 'integer',
  'column2', 'b', 1, 'integer',
  'pretty', 'p', 1, 'logical',
  'ellipse', 'e', 1, 'logical',
  'tokens', 't', 1, 'logical',
  'means', 'm', 1, 'logical'
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
with(data,plotVowels(f1, f2, vowel, plot.tokens = options$tokens, pch.tokens = vowel, cex.tokens = 1.2, 
                     alpha.tokens = 0.2, plot.means = options$means, pch.means = vowel, cex.means = 2, var.col.by = vowel, 
                     ellipse.line = options$ellipse, pretty = options$pretty))

dev.off();
htmlfile_handle <- file(htmlfile)
html_output = c('<html><body>',
                '<h3>Result:</h3><img src="pngfile.png"/>',
                '<a download="pngfile.png" href="pngfile.png" title="VowelPlot" type="button">Download Plot</a>',
                '</html></body>');
writeLines(html_output, htmlfile_handle);
close(htmlfile_handle);
