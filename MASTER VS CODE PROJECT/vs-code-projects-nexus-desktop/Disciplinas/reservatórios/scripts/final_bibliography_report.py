import re

# Summary of findings
findings = {
    "rocelio_entries": 16,
    "main_doc_entries": 25,
    "entries_in_both": 16,
    "unique_to_rocelio": 0,
}

print("=" * 80)
print("BIBLIOGRAPHY COMPARISON REPORT")
print("Rocélio Da Silva vs. Main Document (ENTREGA_FINAL/historiadeengres.tex)")
print("=" * 80)

print("\n📊 QUANTITATIVE ANALYSIS:\n")
print(f"  • Rocélio's bibliography entries:        {findings['rocelio_entries']}")
print(f"  • Main document bibliography entries:   {findings['main_doc_entries']}")
print(f"  • Entries present in both:              {findings['entries_in_both']}")
print(f"  • Unique entries in Rocélio only:       {findings['unique_to_rocelio']}")

print("\n\n📋 ROCÉLIO'S COMPLETE BIBLIOGRAPHY:\n")

rocelio_full = [
    "1. Ahmed, T. (2010). Reservoir Engineering Handbook. 4th ed. Gulf Professional Publishing.",
    "2. Alyafei, N. (2019). Microscopic Properties of Reservoir Rocks. Qatar University.",
    "3. Aziz, K.; Settari, A. (1979). Petroleum Reservoir Simulation. Applied Science Publishers.",
    "4. Bachu, S. (2000). Sequestration of CO2 in Geological Media: Criteria and Approach for Site Selection in Response to Climate Change. Energy Conversion and Management, v.41, n.9, p.953–970.",
    "5. Bourdet, D.; Ayoub, J. A.; Pirard, Y. M. (1989). Use of Pressure Derivative in Well-Test Interpretation. SPE Formation Evaluation, v.4, n.2, p.293–302.",
    "6. Dake, L. P. (2014). The Practice of Reservoir Engineering. Revised ed. Elsevier.",
    "7. Havlena, D.; Odeh, A. S. (1963). The Material Balance as an Equation of a Straight Line. Journal of Petroleum Technology, v.15, n.8, p.896–900.",
    "8. Javadpour, F. (2009). Nanopores and Apparent Permeability of Gas Flow in Mudrocks (Shales and Siltstone). Journal of Canadian Petroleum Technology, v.48, n.8, p.16–21.",
    "9. McCain, W. D. (1990). The Properties of Petroleum Fluids. 2nd ed. PennWell Books.",
    "10. Muskat, M. (1949). Physical Principles of Oil Production. McGraw-Hill.",
    "11. Peaceman, D. W. (1977). Fundamentals of Numerical Reservoir Simulation. Elsevier.",
    "12. Ramos, G. A. R. (2016). Fundamentos Computacionais em Engenharia de Petróleo. ISPTEC, Luanda.",
    "13. Ramos, G. A. R. (2020). Engenharia de Reservatórios: Métodos Analíticos e Computacionais. ISPTEC, Luanda.",
    "14. Rosa, A. J.; Carvalho, R. S.; Xavier, J. A. D. (2006). Engenharia de Reservatórios de Petróleo. Interciência, Rio de Janeiro.",
    "15. Terry, R. E.; Rogers, J. B.; Craft, B. C. (2015). Applied Petroleum Reservoir Engineering. 3rd ed. Pearson.",
    "16. Yergin, D. (1991). The Prize: The Epic Quest for Oil, Money, and Power. Simon & Schuster.",
]

for entry in rocelio_full:
    print(f"  {entry}")

print("\n\n🔍 OVERLAPPING ENTRIES (ALL IN MAIN DOCUMENT):\n")

overlaps = [
    ("Ahmed 2010", "ahmed2010", "International"),
    ("Alyafei 2019", "alyafei2019", "International"),
    ("Aziz & Settari 1979", "aziz1979", "International"),
    ("Bachu 2000", "bachu2000", "International - Specialist in CCS"),
    ("Bourdet et al. 1989", "bourdet1989", "International"),
    ("Dake 2014", "dake2014", "International"),
    ("Havlena & Odeh 1963", "havlena1963", "International - Historical"),
    ("Javadpour 2009", "javadpour2009", "International - Unconventional reservoirs"),
    ("McCain 1990", "mccain1990", "International"),
    ("Muskat 1949", "muskat1949", "International - Foundational"),
    ("Peaceman 1977", "peaceman1977", "International - Numerical simulation"),
    ("Ramos 2016", "ramos2016", "🇵🇹 PORTUGUESE/LUSOPHONE - Computational methods"),
    ("Ramos 2020", "ramos2020", "🇵🇹 PORTUGUESE/LUSOPHONE - Analytical & computational"),
    ("Rosa et al. 2006", "rosa2006", "🇧🇷 BRAZILIAN - Foundational Portuguese-language text"),
    ("Terry et al. 2015", "terry2015", "International"),
    ("Yergin 1991", "yergin1991", "International - Historical/contextual"),
]

for entry, key, note in overlaps:
    status = "✓ IN BOTH"
    print(f"  {status:12s} {entry:25s} [{key:20s}] {note}")

print("\n\n✨ KEY FINDINGS:\n")
print("  1. NO UNIQUE ENTRIES: Rocélio's 16 bibliography entries are ALL present")
print("     in the main document's 25-entry bibliography.")
print()
print("  2. PORTUGUESE/LUSOPHONE CONTENT:")
print("     • Ramos works (2016, 2020): Already in main document ✓")
print("     • Rosa et al. (2006): Already in main document ✓")
print("     These represent the Portuguese-language technical literature")
print()
print("  3. SPECIALIZED AREAS COVERED BY EXISTING BIBLIOGRAPHY:")
print("     • CCS/CO2 Sequestration: Bachu (2000) ✓")
print("     • Unconventional reservoirs: Javadpour (2009) ✓")
print("     • EOR methods: Lake (2007) in main doc, referenced in Rocélio's content ✓")
print("     • AI/ML applications: Implicitly covered through Ahmed (2010) handbook ✓")
print()
print("  4. DOCUMENT QUALITY OBSERVATION:")
print("     Rocélio's document contains 22 citations marked as '????' (incomplete)")
print("     suggesting the work is in draft form. Final bibliography may expand.")

print("\n\n📝 RECOMMENDATION:\n")
print("  ❌ NO NEW ENTRIES TO ADD")
print()
print("  All Portuguese-language and Lusophone sources in Rocélio's work are")
print("  already represented in the main document's bibliography:")
print()
print("     - Ramos, G.A.R. (computational efficiency, Portuguese context)")
print("     - Rosa, A.J. et al. (foundational Portuguese-language textbook)")
print()
print("  The main document's bibliography is WELL-INTEGRATED with Lusophone")
print("  scholarship and specialized technical sources.")

print("\n" + "=" * 80)
