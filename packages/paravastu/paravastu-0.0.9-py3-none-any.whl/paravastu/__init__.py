from biopandas.pdb import PandasPdb
import pandas
import numpy
import dtale
import glob
import os
import sys
from math import pi

def ReadPDBintoDataFrame(PDBfileNameString):
    t= PandasPdb().read_pdb(PDBfileNameString).df["ATOM"]
    df = pandas.DataFrame(t)
    f = open(PDBfileNameString,'r')
    text = f.readlines()
    f.close()
    df.text = text
    df.path = PDBfileNameString
    return df 
def RetreivePDBatomPosition(dataFramePDB, segmentIDstring, residueNumber, atomNameString):
    df1 = dataFramePDB.loc[dataFramePDB["segment_id"]== segmentIDstring]
    df1= df1.loc[dataFramePDB["residue_number"]==residueNumber]
    df1 = df1.loc[dataFramePDB["atom_name"]==atomNameString]
    df1= df1[["x_coord", "y_coord","z_coord"]]
    return df1.to_numpy()
def PDBsegmentIDset(dataFramePDB):
    segmentSet = dataFramePDB.segment_id.unique()
    return segmentSet
def EuclideanDistance(coords1, coords2):
    return numpy.linalg.norm(coords1-coords2)

protein_letters = "ACDEFGHIKLMNPQRSTVWY"
extended_protein_letters = "ACDEFGHIKLMNPQRSTVWYBXZJUO"
protein_letters_1to3 = {
    "A": "Ala",
    "C": "Cys",
    "D": "Asp",
    "E": "Glu",
    "F": "Phe",
    "G": "Gly",
    "H": "His",
    "I": "Ile",
    "K": "Lys",
    "L": "Leu",
    "M": "Met",
    "N": "Asn",
    "P": "Pro",
    "Q": "Gln",
    "R": "Arg",
    "S": "Ser",
    "T": "Thr",
    "V": "Val",
    "W": "Trp",
    "Y": "Tyr",
}
protein_letters_1to3_extended = dict(
    list(protein_letters_1to3.items())
    + list(
        {"B": "Asx", "X": "Xaa", "Z": "Glx", "J": "Xle", "U": "Sec", "O": "Pyl"}.items()
    )
)

protein_letters_3to1 = {x[1]: x[0] for x in protein_letters_1to3.items()}
protein_letters_3to1_extended = {
    x[1]: x[0] for x in protein_letters_1to3_extended.items()
}

def ConvertToOneLetter(seq, custom_map=None, undef_code="X"):

    if custom_map is None:
        custom_map = {"Ter": "*"}
    # reverse map of threecode
    # upper() on all keys to enable caps-insensitive input seq handling
    onecode = {k.upper(): v for k, v in protein_letters_3to1_extended.items()}
    # add the given termination codon code and custom maps
    onecode.update((k.upper(), v) for k, v in custom_map.items())
    seqlist = [seq[3 * i : 3 * (i + 1)] for i in range(len(seq) // 3)]
    return "".join(onecode.get(aa.upper(), undef_code) for aa in seqlist)

def ConvertToThreeLetter(seq, custom_map=None, undef_code="Xaa"):
    if custom_map is None:
        custom_map = {"*": "Ter"}
    # not doing .update() on IUPACData dict with custom_map dict
    # to preserve its initial state (may be imported in other modules)
    threecode = dict(
        list(protein_letters_1to3_extended.items()) + list(custom_map.items())
    )
    # We use a default of 'Xaa' for undefined letters
    # Note this will map '-' to 'Xaa' which may be undesirable!
    return "".join(threecode.get(aa, undef_code) for aa in seq)

def GetHydrogenBondDistances(dataFramePDB, resstart, resstop):
    segments = PDBsegmentIDset(dataFramePDB)
    index = [i for i  in range(0, len(segments))]
    segstart = index[0]
    segstop = index[-1]
    residues2check = numpy.arange(resstart, resstop+1, 2)
    HBondDistances= numpy.zeros((segstop-segstart, len(residues2check)))
    for i in range(segstart, segstop):
        for j in residues2check:
            HN = RetreivePDBatomPosition(dataFramePDB, segments[i+1],j+1,'HN')
            CO = RetreivePDBatomPosition(dataFramePDB, segments[i],j,'O')
            HBondDistances[i-1, int(numpy.where(residues2check == j)[0])]=EuclideanDistance(HN, CO)
    return HBondDistances

def FindAngle(u,v):
    """
    Calculates the angle (degrees) between two vectors (as 1-d arrays) using
    dot product.
    """

    V1 = u / numpy.linalg.norm(u)
    V2 = v/ numpy.linalg.norm(v)
    return 180/pi * numpy.arccos(numpy.dot(V1,V2))

def CalcDihedrals(prevCO,currN,currCA,currCO,nextN,cutoff=6.5):
    """
    Calculates phi and psi angles for an individual residue.
    """

    # Set CA coordinates to origin
    A = [prevCO[i] - currCA[i] for i in range(3)]
    B = [currN[i] - currCA[i] for i in range(3)]
    C = [currCO[i] - currCA[i] for i in range(3)]
    D = [nextN[i] - currCA[i] for i in range(3)]

    # Make sure the atoms are close enough
    #if max([dist_sq(x) for x in [A,B,C,D]]) > cutoff:
    #    err = "Atoms too far apart to be bonded!"
    #    raise ValueError(err)

    # Calculate necessary cross products (define vectors normal to planes)
    V1 = numpy.cross(A,B)
    V2 = numpy.cross(C,B)
    V3 = numpy.cross(C,D)

    # Determine scalar angle between normal vectors
    phi = FindAngle(V1,V2)
    if numpy.dot(A,V2) > 0: phi = -phi

    psi = FindAngle(V2,V3)
    if numpy.dot(D,V2) < 0: psi = -psi

    return phi, psi




def CalculateTorsion(pdbDataFrame):
    """
    Calculate the backbone torsion angles for a pdb file.
    """
    pdb = pdbDataFrame.text
    residue_list = []
    N = []
    CO = []
    CA = []

    resid_contents = {}
    current_residue = None
    to_take = ["N  ","CA ","C  "]
    for line in pdb:
        if line[0:4] == "ATOM" or (line[0:6] == "HETATM" and line[17:20] == "MSE"):

            if line[13:16] in to_take:

                # First residue
                if current_residue == None:
                    current_residue = line[17:26]
                    print(current_residue)
                    #added print statement

                # If we're switching to a new residue, record the previously
                # recorded one.
                if current_residue != line[17:26]:

                    try:
                        N.append([float(resid_contents["N  "][30+8*i:38+8*i])
                                  for i in range(3)])
                        CO.append([float(resid_contents["C  "][30+8*i:38+8*i])
                                   for i in range(3)])
                        CA.append([float(resid_contents["CA "][30+8*i:38+8*i])
                                   for i in range(3)])
                        residue_list.append(current_residue)

                    except KeyError:
                        err = "Residue %s has missing atoms: skipping.\n" % current_residue
                        sys.stderr.write(err)

                    # Reset resid contents dictionary
                    current_residue = line[17:26]
                    resid_contents = {}

                # Now record N, C, and CA entries.  Take only a unique one from
                # each residue to deal with multiple conformations etc.
                if line[13:16] not in resid_contents:
                    resid_contents[line[13:16]] = line
                else:
                    err = "Warning: %s has repeated atoms!\n" % current_residue
                    sys.stderr.write(err)

    # Record the last residue
    try:
        N.append([float(resid_contents["N  "][30+8*i:38+8*i])
                  for i in range(3)])
        CO.append([float(resid_contents["C  "][30+8*i:38+8*i])
                   for i in range(3)])
        CA.append([float(resid_contents["CA "][30+8*i:38+8*i])
                   for i in range(3)])
        residue_list.append(current_residue)

    except KeyError:
        err = "Residue %s has missing atoms: skipping.\n" % current_residue
        sys.stderr.write(err)


    # Calculate phi and psi for each residue.  If the calculation fails, write
    # that to standard error and move on.
    labels = []
    dihedrals = []
    for i in range(1,len(residue_list)-1):
        try:
            dihedrals.append(CalcDihedrals(CO[i-1],N[i],CA[i],CO[i],
                                                    N[i+1]))
            labels.append(residue_list[i])
        except ValueError:
            err = "Dihedral calculation failed for %s\n" % residue_list[i]
            sys.stderr.write(err)
    torsion_angles = pandas.DataFrame(dihedrals, columns = ["Phi", "Psi"])
    torsion_angles["Residue Name, Chain ID, Residue Number"] = labels
    return torsion_angles


def Display(DataFrame):
    DisplayFrame = dtale.show(DataFrame)
    return DisplayFrame

def ListFileType(FileType):
    for file in glob.glob(FileType):
        print(file)

def ListDirectory():
    files = os.listdir(os.getcwd())
    for f in files:
	    print(f)




  