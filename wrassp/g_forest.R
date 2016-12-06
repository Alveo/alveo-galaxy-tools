
library(wrassp)

args = commandArgs(TRUE)
# args will be like
#        ${wavfile} ${output}
#        ${beginTime} ${endTime} ${windowShift} ${windowSize} ${effectiveLength}
#        ${nominalF1} ${gender} ${estimate} ${order} ${incrOrder} ${numFormants}
#        ${window} ${preEmphasis}


if (length(args) != 15) {
    print("Wrong number of arguments!")
    q("no", status=1)
}

res = forest(args[1], toFile=FALSE, beginTime=as.numeric(args[3]), endTime=as.numeric(args[4]),
             windowShift=as.numeric(args[5]),
             windowSize=as.numeric(args[6]),
             effectiveLength=as.integer(args[7]),
             nominalF1=as.numeric(args[8]),
             gender=args[9],
             estimate=as.integer(args[10]),
             order=as.numeric(args[11]), incrOrder=as.numeric(args[12]),
             numFormants=as.numeric(args[13]), window=args[14],
             preemphasis=as.numeric(args[15])
             )

assp_to_tsv(res, args[2])
