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
        self.periodepaie = ""
        self.raisonsoc = ""

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

    def param_dossier(self):
        """Paramètres des établissements"""
        sql = """
            SELECT CodeEtablissement, RaisonSocial, PeriodePaie 
            FROM Etablissements
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()




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
    o.disconnect()

