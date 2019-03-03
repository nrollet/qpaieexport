import logging
import pyodbc
from datetime import datetime


class QueryPaie(object):
    """
    Submit queries to Quadra Paie database in MS Access format
    """

    def __init__(self):

        self.conx = ""
        self.mdbpath = ""
        self.param = {}
        self.periodepaie = ""
        self.databull = []
        self.dataemp = []

        # self.raisonsoc = ""

    def connect(self, mdbpath):

        self.mdbpath = mdbpath.lower()

        constr = "Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=" + self.mdbpath
        try:
            self.conx = pyodbc.connect(constr, autocommit=True)
            self.cursor = self.conx.cursor()
        except pyodbc.Error as msg:
            logging.error(msg)
            return False
        return True

    def disconnect(self):
        self.conx.commit()
        self.conx.close()

    # def periodepaie(self):
    # sql = """SELECT PeriodePaie FROM ConstantesEntreprise"""
    # self.cursor.execute(sql)
    # self.periodepaie = self.cursor.fetchall()[0]

    def param_dossier(self):
        """requête pour les paramètres des établissements"""
        sql = "SELECT CodeEtablissement, RaisonSociale FROM Etablissements"
        self.cursor.execute(sql)
        for etab, rs in self.cursor.fetchall():
            self.param.update({"etab": {"rs": rs, "code": etab}})

        sql = """SELECT PeriodePaie FROM ConstantesEntreprise"""
        self.cursor.execute(sql)
        self.periodepaie = self.cursor.fetchall()[0][0]
        # self.param.update({"periode": self.cursor.fetchall()[0]})

        return self.param

    def employes(self):
        sql = """
            SELECT EM.Numero, EM.NomNaissance, 
            EM.NomMarital, EM.Prenom, 
            EM.DateEntree1, EM.DateEntree2,
            EM.DateSortie1, EM.DateSortie2
            FROM Employes EM 
            INNER JOIN CriteresLibres CL
            ON EM.Numero=CL.NumeroEmploye
            """

        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        for (
            Numero,
            NomNaissance,
            NomMarital,
            Prenom,
            DateEntree1,
            DateEntree2,
            DateSortie1,
            DateSortie2,
        ) in data:
            numero = Numero.lstrip()
            nom = NomNaissance
            if NomMarital:
                nom = NomMarital
            nom = nom + " " + Prenom
            entree = DateEntree1
            if DateEntree2 > DateEntree1:
                entree = DateEntree2
            sortie = DateSortie1
            if DateSortie1 and DateEntree2 == "":
                sortie = DateSortie1
            elif DateSortie2:
                sortie = DateSortie2
            if entree == datetime(1899, 12, 30, 0, 0):
                entree = None
            if sortie == datetime(1899, 12, 30, 0, 0):
                sortie = None

            self.dataemp.append([numero, nom, entree, sortie])

        return self.dataemp

    def collecte_bulletins(self):
        """requête pour les données des bulletins"""
        sql = "SELECT * FROM Bulletins"

        self.cursor.execute(sql)
        self.databull = self.cursor.fetchall()
        return self.databull


if __name__ == "__main__":

    import pprint
    import logging

    pp = pprint.PrettyPrinter(indent=4)
    logging.basicConfig(
        level=logging.DEBUG, format="%(funcName)s\t\t%(levelname)s - %(message)s"
    )

    mdbpath = "C:/Users/nicolas/Documents/Pydio/Sources/odenval_qpaie.mdb"
    o = QueryPaie()
    if o.connect(mdbpath):
        logging.info("success")
    pp.pprint(o.param_dossier())
    # pp.pprint(o.employes())
    pp.pprint(o.periodepaie)
    pp.pprint(o.collecte_bulletins())
    o.disconnect()

