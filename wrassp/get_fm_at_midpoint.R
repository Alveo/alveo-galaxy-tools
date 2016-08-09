
library(wrassp)

get_fm_at_midpoint <- function(segments, wavmap) {
    midpoint_fm <- function(row) {
        start = as.numeric(row[1])
        end = as.numeric(row[2])
        identifier = row[5]
        fn = wavmap[identifier]
        if (is.na(fn)) {
            cat("Can't find wav file for ", identifier, "\n")
            return(c(0,0,0,0))
        } else {
            res = forest(fn, beginTime=start, endTime=end, toFile=FALSE)
            return(res$fm[nrow(res$fm)/2,])
        }
    }

    print(wavmap)

    fm = t(apply(segments, 1, midpoint_fm))
    fm = data.frame(fm=fm, labels=segments$label, identifier=segments$identifier)

    return(fm)
}

args = commandArgs(TRUE)
# args will be like
# qresult.dat outfile.dat --wavfile a,b,c --identifier A,B,C
# need to split out wavfile and identifier args on ,

if (length(args) != 6) {
    print("Wrong number of arguments!")
    exit(1)
}

segmentfile = args[1]
wavfiles = args[4]
identifiers = args[6]
outfile = args[2]

# split on comma
wavfiles = strsplit(wavfiles, ",")[[1]]
identifiers = strsplit(identifiers, ",")[[1]]

if( length(wavfiles) != length(identifiers)) {
    print("Lengths of wavfiles and identifiers don't match.")
    exit(1)
}
cat("\nWAVMAP\n")
wavmap = NULL
for(i in 1:length(wavfiles)) {
    wavmap[identifiers[i]] = wavfiles[i]
}

segments = read.table(segmentfile, header=TRUE)

result = get_fm_at_midpoint(segments, wavmap)

write.table(result, file=outfile, sep="\t", quote=F, row.names=F)
