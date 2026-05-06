import re

# Rocélio's bibliography (extracted from PDF)
rocelio_bib = """
AHMED,T.ReservoirEngineeringHandbook.4thed.GulfProfessionalPublishing,2010.
ALYAFEI,N.MicroscopicPropertiesofReservoirRocks.QatarUniversity,2019.
AZIZ,K.;SETTARI,A.PetroleumReservoirSimulation.AppliedSciencePublishers,1979.
BACHU,S.SequestrationofCO2inGeologicalMedia:CriteriaandApproachforSiteSelection
inResponsetoClimateChange.EnergyConversionandManagement,v.41,n.9,p.953–970,
2000.
BOURDET,D.;AYOUB,J.A.;PIRARD,Y.M.UseofPressureDerivativeinWell-Test
Interpretation.SPEFormationEvaluation,v.4,n.2,p.293–302,1989.
DAKE,L.P.ThePracticeofReservoirEngineering.Reviseded.Elsevier,2014.
HAVLENA,D.;ODEH,A.S.TheMaterialBalanceasanEquationofaStraightLine.Journal
ofPetroleumTechnology,v.15,n.8,p.896–900,1963.
JAVADPOUR,F.NanoporesandApparentPermeabilityofGasFlowinMudrocks(Shalesand
Siltstone).JournalofCanadianPetroleumTechnology,v.48,n.8,p.16–21,2009.
McCAIN,W.D.ThePropertiesofPetroleumFluids.2nded.PennWellBooks,1990.
MUSKAT,M.PhysicalPrinciplesofOilProduction.McGraw-Hill,1949.
PEACEMAN,D.W.FundamentalsofNumericalReservoirSimulation.Elsevier,1977.
RAMOS,G.A.R.FundamentosComputacionaisemEngenhariadePetróleo.ISPTEC,Luanda,
2016.
RAMOS,G.A.R.EngenhariadReservatórios:MétodosAnalíticoseComputacionais.
ISPTEC,Luanda,2020.
ROSA,A.J.;CARVALHO,R.S.;XAVIER,J.A.D.EngenhariadeReservatóriosdePetróleo.
Interciência,RiodeJaneiro,2006.
TERRY,R.E.;ROGERS,J.B.;CRAFT,B.C.AppliedPetroleumReservoirEngineering.3rded.
Pearson,2015.
YERGIN,D.ThePrize:TheEpicQuestforOil,Money,andPower.Simon&Schuster,1991.
"""

# Main document references (from referencias.bib)
main_bib_entries = {
    'rosa2006': {'author': 'Rosa, A. J. and Carvalho, R. S. and Xavier, J. A. D.', 'year': 2006},
    'dake2014': {'author': 'Dake, L. P.', 'year': 2014},
    'mccain1990': {'author': 'McCain, W. D.', 'year': 1990},
    'ahmed2010': {'author': 'Ahmed, T.', 'year': 2010},
    'terry2015': {'author': 'Terry, R. E. and Rogers, J. B. and Craft, B. C.', 'year': 2015},
    'alyafei2019': {'author': 'Alyafei, N.', 'year': 2019},
    'ramos2016': {'author': 'Ramos, G. A. R.', 'year': 2016},
    'ramos2020': {'author': 'Ramos, G. A. R.', 'year': 2020},
    'yergin1991': {'author': 'Yergin, D.', 'year': 1991},
    'havlena1963': {'author': 'Havlena, D. and Odeh, A. S.', 'year': 1963},
    'bourdet1989': {'author': 'Bourdet, D. and Ayoub, J. A. and Pirard, Y. M.', 'year': 1989},
    'javadpour2009': {'author': 'Javadpour, F.', 'year': 2009},
    'bachu2000': {'author': 'Bachu, S.', 'year': 2000},
    'muskat1949': {'author': 'Muskat, M.', 'year': 1949},
    'peaceman1977': {'author': 'Peaceman, D. W.', 'year': 1977},
    'aziz1979': {'author': 'Aziz, K. and Settari, A.', 'year': 1979},
    'lake2007': {'author': 'Lake, L. W.', 'year': 2007},
    'craft1991': {'author': 'Craft, B. C. and Hawkins, M. F. and Terry, R. E.', 'year': 1991},
    'dake1994': {'author': 'Dake, L. P.', 'year': 1994},
    'mungan2019': {'author': 'Mungan, N.', 'year': 2019},
    'spe2015': {'author': 'Society of Petroleum Engineers', 'year': 2015},
    'bp2023': {'author': 'BP', 'year': 2023},
    'eia2023': {'author': 'U.S. Energy Information Administration', 'year': 2023},
    'wikipediaReservoirEngineering': {'author': 'Wikipedia', 'year': 'N/A'},
}

# Extract Rocélio's entries
rocelio_entries = [
    ('Ahmed, T.', 2010),  # Ahmed - 2010
    ('Alyafei, N.', 2019),  # Alyafei - 2019
    ('Aziz, K.; Settari, A.', 1979),  # Aziz & Settari - 1979
    ('Bachu, S.', 2000),  # Bachu - 2000
    ('Bourdet, D.; Ayoub, J. A.; Pirard, Y. M.', 1989),  # Bourdet et al. - 1989
    ('Dake, L. P.', 2014),  # Dake - 2014
    ('Havlena, D.; Odeh, A. S.', 1963),  # Havlena & Odeh - 1963
    ('Javadpour, F.', 2009),  # Javadpour - 2009
    ('McCain, W. D.', 1990),  # McCain - 1990
    ('Muskat, M.', 1949),  # Muskat - 1949
    ('Peaceman, D. W.', 1977),  # Peaceman - 1977
    ('Ramos, G. A. R.', 2016),  # Ramos - 2016
    ('Ramos, G. A. R.', 2020),  # Ramos - 2020
    ('Rosa, A. J.; Carvalho, R. S.; Xavier, J. A. D.', 2006),  # Rosa et al. - 2006
    ('Terry, R. E.; Rogers, J. B.; Craft, B. C.', 2015),  # Terry et al. - 2015
    ('Yergin, D.', 1991),  # Yergin - 1991
]

print("=== COMPARISON: ROCÉLIO'S BIBLIOGRAPHY vs MAIN DOCUMENT ===\n")

# Check each Rocélio entry
entries_in_both = []
unique_to_rocelio = []

for author, year in rocelio_entries:
    found_in_main = False
    for key, entry in main_bib_entries.items():
        if entry['year'] == year and author.split(';')[0].strip() in entry['author']:
            found_in_main = True
            entries_in_both.append((author, year, key))
            break
    
    if not found_in_main:
        unique_to_rocelio.append((author, year))

print(f"Rocélio entries in main document: {len(entries_in_both)}")
print(f"Potentially unique entries: {len(unique_to_rocelio)}")
print()

if unique_to_rocelio:
    print("=== ENTRIES ONLY IN ROCÉLIO'S BIBLIOGRAPHY ===\n")
    for author, year in unique_to_rocelio:
        print(f"- {author} ({year})")
else:
    print("All entries in Rocélio's bibliography are already in the main document.")

print("\n=== ENTRIES IN BOTH ===\n")
for author, year, main_key in entries_in_both:
    print(f"✓ {author} ({year}) - Key: {main_key}")
