assp_to_tsv <- function(assp, outfile) {

    # convert to a dataframe, need to add one column at a time
    result <- data.frame(assp[1])
    if (length(attr(assp,'names'))>1) {
        for(idx in seq(2,length(attr(assp,'names')))) {
            result <- cbind(result, assp[idx])
        }
    }
    # add a column of timestamps
    start <- attr(assp, 'startTime')
    rate <- attr(assp, 'sampleRate')
    time <- seq(start, by=1/rate, length.out=nrow(result))
    result <- cbind(time, result)

    write.table(result, file=outfile, sep="\t", quote=F, row.names=F, col.names=T, append=F)
}
