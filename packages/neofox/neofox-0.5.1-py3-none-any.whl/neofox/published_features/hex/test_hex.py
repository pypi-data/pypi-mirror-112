import subprocess
import os
iedb_fasta="/home/franlang/neofox_test/test_references_nets/iedb/IEDB.fasta"

def apply_hex(mut_peptide):
    """this function calls hex tool. this tool analyses the neoepitope candidate sequence for molecular mimicry to viral epitopes
    """
    my_path = os.path.abspath(os.path.dirname(__file__))
    model_path = os.path.join(my_path, "hexR")
    hex_path = os.path.join(my_path, "hexR")
    tool_path = os.path.join(hex_path, "hex.R")
    cmd = ["Rscript", tool_path, mut_peptide, iedb_fasta, hex_path]
    cmd = " ".join(cmd).split(" ")
    print(cmd)
    process = subprocess.Popen(
            cmd
            ,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,

        )
    output, errors = process.communicate()
    return output.decode("utf8")


if __name__ == '__main__':
    mut_peptide= "FGLAIDVDD"
    res = apply_hex(mut_peptide)
    a,b = res.split(" ")
    print(a)
    print(b)
