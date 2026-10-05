# read EGENVAL.OUT file from Elk
with open("EIGENVAL.OUT", "r", encoding="utf-8") as f:
    lines = f.readlines()

hartree_to_ev = 27.21138624598

# take only the first part of the first and second line which contains the number of kpoints and bands
nkpoints = lines[0].split()[0]
nbands = lines[1].split()[0]
# figure out how to make these not a hardcoded value
nions = 2 
nblock_kblock = 1
temp = 1.0e-4

def get_eigenvals(output_file):
    nelec = 0
    kpoint_index = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "k-point" in line:
            kpoint_index = line.split()[0]
            if kpoint_index != "1":
                break
        elif kpoint_index == "1":
            if "nkpt" in line or "nstsv" in line or "state" in line:
                continue
            band_num = line.split()[0]
            if band_num == "1":
                occ = line.split()[2]
                if float(occ) == 2.0:
                    spin_pol = 1
                else:
                    spin_pol = 2

            elec = line.split()[2]
            nelec += int(float(elec))

    output_file.write(str(nions) + " " + str(nions) + " " + str(nblock_kblock) + " " + str(spin_pol) + "\n")
    output_file.write(str(temp) + "\n")
    output_file.write(str(nelec) + " " + nkpoints + " " + nbands + "\n\n")

    for line in lines:
        line = line.strip() # removes new line character and extra whitespace
        if line:
            # skip header 
            if "nkpt" in line or "nstsv" in line or "state" in line:
                continue
            elif "k-point" in line:
                # kpoint info
                kpoint_info = line.split()
                kpoint_index = kpoint_info[0]
                kpoint_coords = [a for a in kpoint_info[1:4]]
                out_line = kpoint_coords[0] + " " + kpoint_coords[1] + " " + kpoint_coords[2]
                output_file.write("\n")
            else:
                band_info = line.split()
                band_number = band_info[0]
                eigenval = str(float(band_info[1]) * hartree_to_ev)
                occupancy = float(band_info[2])
                out_line = band_number + " " + eigenval + " " + str(occupancy)
            output_file.write(out_line + "\n")
        else:
            continue

with open("EIGEN_VASP", "w", encoding="utf-8") as output_file:
    get_eigenvals(output_file)