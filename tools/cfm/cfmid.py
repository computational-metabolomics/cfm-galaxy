import argparse
import csv
import os
import shutil


parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--db_local")
parser.add_argument("--num_highest")
parser.add_argument("--ppm_db")
parser.add_argument("--ppm_mass_tol")
parser.add_argument("--abs_mass_tol")
parser.add_argument("--polarity")
parser.add_argument("--score_type")
parser.add_argument("--results")
parser.add_argument("--tool_directory")

args = parser.parse_args()
print(args)

# Example
# python cfmid.py --abs_mass_tol='0.01' --db_local='test-data/demo_db.tsv' --input='test-data/input.msp' --num_highest='10' --polarity='pos' --ppm_db='10.0' --ppm_mass_tol='10.0' --results='results.txt' --score_type='Jaccard' --tool_directory='/home/rw/Documents/cfm-galaxy/tools/cfm'

id2info = {}
mz2id = []
# store DB in dicts
with open(args.db_local) as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter="\t")
    for row in csvreader:
        id2info[row["Identifier"]] = row
        mz2id.append((float(row["MonoisotopicMass"]), row["Identifier"]))

name_tmp = "tmp"
if os.path.isdir(name_tmp):
    shutil.rmtree(name_tmp)

os.makedirs(name_tmp)
with open(args.input, "r") as infile:
    numlines = 0
    for line in infile:
        line = line.strip()
        if numlines == 0:
            print(line)
            if "NAME" in line:
                featid = line.split("NAME: ")[1]
            if "PRECURSORMZ" in line:
                mz = float(line.split("PRECURSORMZ: ")[1])
                if args.polarity == "pos":
                    mz2 = mz - 1.007276
                else:
                    mz2 = mz + 1.007276
            if "Num Peaks" in line:
                numlines = int(line.split("Num Peaks: ")[1])
                linesread = 0
                peaklist = []
        else:
            if linesread == numlines:
                numlines = 0
                cand_id_list = []
                mz_ranges = (float(args.ppm_db) * mz2) / 1e6
                mz_ranges = (mz2 - mz_ranges, mz2 + mz_ranges)
                # check hits
                for t in mz2id:
                    if (t[0] > mz_ranges[0]) and (t[0] < mz_ranges[1]):
                        cand_id_list.append(t[1])
                # run only if we got candidates
                if len(cand_id_list) > 0:
                    # write spec file
                    with open("./tmpspec.txt", "w") as outfile:
                        for e in ["low", "mid", "high"]:
                            outfile.write(e + "\n")
                            for p in peaklist:
                                outfile.write(p[0] + "\t" + p[1] + "\n")
                    # write candidates file
                    with open("./tmpcand.txt", "w") as outfile:
                        for c in cand_id_list:
                            outfile.write(
                                "{0} {1}\n".format(c, id2info[c]["InChI"])
                            )  # TODO: Use InChI or SMILES

                    # create command line call
                    outi = os.path.join(name_tmp, "cfm_" + featid + ".txt")
                    cmd_command = "cfm-id tmpspec.txt {0} tmpcand.txt ".format(featid)
                    cmd_command += "{0} {1} {2} {3} ".format(
                        args.num_highest,
                        args.ppm_db,
                        args.ppm_mass_tol,
                        args.abs_mass_tol,
                    )
                    if args.polarity == "pos":
                        cmd_command += (
                            os.path.join(
                                args.tool_directory,
                                "data",
                                "positive_metab_se_cfm",
                                "param_output0.log",
                            )
                            + " "
                        )
                        cmd_command += (
                            os.path.join(
                                args.tool_directory,
                                "data",
                                "positive_metab_se_cfm",
                                "param_config.txt",
                            )
                            + " "
                        )
                    else:
                        cmd_command += (
                            os.path.join(
                                args.tool_directory,
                                "data",
                                "negative_metab_se_cfm/param_output0.log",
                            )
                            + " "
                        )
                        cmd_command += (
                            os.path.join(
                                args.tool_directory,
                                "data",
                                "negative_metab_se_cfm/param_config.txt",
                            )
                            + " "
                        )
                    cmd_command += "{0} 1 {1}".format(args.score_type, outi)
                    # run
                    print(cmd_command)
                    os.system(cmd_command)
            else:
                line = tuple(line.split("\t"))
                linesread += 1
                peaklist.append(line)


# merge outputs
outfiles = os.listdir(name_tmp)
outfiles.sort(key=lambda x: os.path.getmtime(os.path.join(name_tmp, x)))
with open(args.results, "w") as outfile:
    outfile.write("UID\tRank\tScore\tIdentifier\tInChI\n")
    for fname in outfiles:
        fileid = os.path.basename(fname)
        fileid = fileid.split("_")[1]
        fileid = fileid.split(".txt")[0]
        with open(os.path.join(name_tmp, fname)) as infile:
            for line in infile:
                line = line.replace(" ", "\t")
                outfile.write(fileid + "\t" + line)
