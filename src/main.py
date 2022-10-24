import argparse
import normalize
import format_conversion
import os
def main():
    parser = argparse.ArgumentParser(description="Normalize Hi-C files using Knight-Ruiz method.")
    parser.add_argument("hic_id", help="e.g. GM12878")
    parser.add_argument("res", type=int, help="resolution (bp)")
    parser.add_argument("chrom1", help="first chromosome (e.g. 1)")
    args = parser.parse_args()

    print("normalize")
    outpath = normalize.normalize_intra(args.hic_id, args.res, args.chrom1)
    parent = os.path.dirname(outpath)
    print(parent)
    print("get heatmap")
    chrom = format_conversion.chromFromBed(outpath)
    matrix = format_conversion.matrixFromBed(chrom, outpath, parent)
    print("calculate dist")
    dist = format_conversion.contactToDist(matrix, 0.3, chrom, parent)
    

if __name__ == "__main__":
    main()