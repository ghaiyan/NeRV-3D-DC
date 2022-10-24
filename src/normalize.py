import numpy as np


def get_res_string(res):
    """Converts resolution in bp to string (e.g. 10kb)"""
    res_kb = int(res/1000)
    if res_kb < 1000:
        return str(res_kb) + "kb"
    else:
        return str(res_kb/1000) + "mb"


def normalize(chrom, rawpath, krpath, res, outpath):
    kr = np.loadtxt(krpath)
    with open(rawpath) as raw:
        with open(outpath, "w") as out:
            for line in raw:
                line = line.split()
                loc1 = line[0]
                loc2 = line[1]
                norm1 = kr[int(int(loc1)/res)]
                norm2 = kr[int(int(loc2)/res)]
                if not np.isnan(norm1) and not np.isnan(norm2):
                    out.write("\t".join((chrom, loc1, str(int(loc1) + res), chrom, loc2, str(int(loc2) + res), str(float(line[2])/(norm1 * norm2)))) + "\n")
                # elif np.isnan(norm1) and not np.isnan(norm2):
                #     out.write("\t".join((chrom, loc1, str(int(loc1) + res), chrom, loc2, str(int(loc2) + res), str(float(line[2])/norm2))) + "\n")
                # elif not np.isnan(norm1) and np.isnan(norm2):
                #     out.write("\t".join((chrom, loc1, str(int(loc1) + res), chrom, loc2, str(int(loc2) + res), str(float(line[2])/norm1))) + "\n")
                # else:
                #     out.write("\t".join((chrom, loc1, str(int(loc1) + res), chrom, loc2, str(int(loc2) + res), line[2])) + "\n")
        out.close()
    raw.close()


def normalize_intra(hic_id, res, chrom):
    res_string = get_res_string(res)
    rawpath = "chr{}_{}.RAWobserved".format(chrom, res_string)
    krpath = "chr{}_{}.KRnorm".format(chrom, res_string)
    outpath = "{}_{}_{}.bed".format(hic_id, chrom, res_string)
    chromstring = "chr" + chrom
    normalize(chromstring, rawpath, krpath, res, outpath)
    return outpath
