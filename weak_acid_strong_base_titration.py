from reaktoro import *

from numpy import linspace,zeros,append

import matplotlib.pyplot as plt

#Problem parameters

steps = 100 #Number of calculation steps. Increases computing time.

acid = 'H3PO4(aq)'

base = 'NaOH(aq)'

MW_acid = 97.994 #g/mol

MW_base = 39.997 #g/mol

molarity_acid  = 1 #mol/L_acid_dis

molarity_base = 0.5  #mol/L_base_dis

V_base_dis = 2 #L_base_dis

T = 25

T_units = 'celsius'

P = 1 

P_units = 'atm'

density_dis_estimated = 1000 #g/L

V_acid_dis = numpy.linspace(0,2, steps) #Acid dis volume samples

pH_array = []

#Iterations

for i in range(steps):

#Calculations
    
    V_acid_dis_star = V_acid_dis[i]

    n_acid = molarity_acid * V_acid_dis_star #mol_acid
    
    n_base = molarity_base * V_base_dis #mol_base
    
    m_acid_dis = density_dis_estimated * V_acid_dis_star #g_acid_dis
    
    m_water_acid = m_acid_dis - MW_acid * V_acid_dis_star  #g_water
    
    m_base_dis = density_dis_estimated * V_base_dis #g_base_dis
    
    m_water_base = m_base_dis - MW_base * V_base_dis #g_water
    
    m_water_total = m_water_acid + m_water_base #g_water
    
    
    #Initialize a thermodynamic database
    
    db = Database('supcrt98.xml')
    
    
    #Define the chemical system
    
    editor = ChemicalEditor(db)
    
    editor.addAqueousPhase("H3PO4(aq) H2PO4- HPO4-- PO4--- NaOH(aq) Na+ H+ OH- H2O(l)")
    
    editor.addGaseousPhase(['H2O(g)'])
    
    
    #Construct the chemical system
    
    system = ChemicalSystem(editor)
    
    
    # Define the chemical equilibrium problem
    
    problem = EquilibriumProblem(system)
    
    problem.setTemperature(T, T_units)
    
    problem.setPressure(P, P_units)
    
    problem.add('H2O', m_water_total, 'g')
    
    problem.add('H3PO4', n_acid, 'mol')
    
    problem.add('NaOH', n_base, 'mol')
    
    
    #Calculate the chemical equilibrium state
    
    state = equilibrate(problem)
    
    
    #Output the calculated chemical state to a file
    
    properties = state.properties()
    
    evaluate_pH = ChemicalProperty.pH(system)
    
    pH = evaluate_pH(properties)
    
    pH_val = pH.val
    
    pH_array = numpy.append(pH_array, pH_val)

plt.figure(1)

title = str(acid + str(molarity_acid) + 'M ' + '  +  ' + base + str(molarity_base) + 'M   ' + str(V_base_dis) + 'L' + '  titration')

plt.plot(V_acid_dis,pH_array,'b-')

plt.xlabel('V_acid_dis [L]')

plt.ylabel('pH [-]')

plt.title(title)

plt.savefig(str(title + '.png'))

