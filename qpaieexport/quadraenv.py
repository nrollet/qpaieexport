import logging

class quadraenv(object):
    def __init__(self, ipl_file):

        self.cpta = ""
        self.paie = ""
        self.gi = ""
        with open(ipl_file, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.rstrip().replace("\\", "/")
            if "=" in line:
                key, item = line.split("=")[0:2]
                if key == "RACDATACPTA":
                    self.cpta = item
                elif key == "RACDATAPAIE":
                    self.paie = item
                elif key == "RACDATAGI":
                    self.gi = item


if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    ipl = "C:/Users/nicolas/Documents/GIT/tdbqpaie/tests/server.ipl"
    o = quadraenv(ipl)
    pp.pprint("---".join([o.cpta, o.paie, o.gi]))
