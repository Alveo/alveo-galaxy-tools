
library(wrassp)

args = commandArgs(TRUE)
# args will be like
#        ${wavfile} ${output}
#        ${beginTime} ${endTime}
#        ${windowShift} ${window} ${resolution}
#        ${fftLength}


if (length(args) != 8) {
    print("Wrong number of arguments!")
    q("no", status=1)
}

res = cepstrum(args[1], toFile=FALSE,
               beginTime=as.numeric(args[3]),
               endTime=as.numeric(args[4]),
               windowShift=as.numeric(args[5]),
               window=args[6],
               resolution=as.numeric(args[7]),
               fftLength=as.numeric(args[8])
             )

assp_to_tsv(res, args[2])
