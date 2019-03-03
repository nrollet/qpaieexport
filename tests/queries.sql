SELECT EM.Numero, EM.NomNaissance, EM.NomMarital, EM.Prenom, 
FROM Employes EM INNER JOIN CriteresLibres CL
    ON EM.Numero=CL.NumeroEmploye
WHERE
((EM.DateSortie1=0 OR EM.DateSortie1>#2/01/2019
#) OR
(EM.DateEntree2<>0 AND
(EM.DateSortie2>#2/01/2019# OR
EM.DateSortie2=0)))

SELECT NumeroEmploye, periode, SBase, Brut, TrancheA,
    TrancheB, TrancheC, BaseSecu,
    TotRetenue, TotCotisPatron,
    NetImpos, NetAPayer, MtNetPayeTheo,
    NbHNormal, NbHTrav, CoutGlobalMois, 

FROM Bulletins