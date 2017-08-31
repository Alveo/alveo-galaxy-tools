
library(wrassp)

args = commandArgs(TRUE)
# args will be like
#        ${wavfile} ${output}
#        ${beginTime} ${endTime} ${windowShift} ${gender} ${maxF} ${minF} ${minAmp} ${maxZCR}



if (length(args) != 10) {
    print("Wrong number of arguments!")
    q("no", status=1)
}

res = ksvF0(args[1], toFile=FALSE, beginTime=as.numeric(args[3]), endTime=as.numeric(args[4]),
             windowShift=as.numeric(args[5]),
             gender=args[6],
             maxF=as.numeric(args[7]),
             minF=as.numeric(args[8]),
             minAmp=as.numeric(args[9]),
             maxZCR=as.numeric(args[10])
             )

assp_to_tsv(res, args[2])
