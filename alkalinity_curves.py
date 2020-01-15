from reaktoro import *

from numpy import linspace,zeros,append

import matplotlib.pyplot as plt

import pandas

#Problem parameters

steps = 1000 #Number of calculation steps. Increases computing time.

acid = 'CO2(g)'

base = 'NH3(g)'

MW_acid = 44.01 #g/mol

MW_base = 17.031  #g/mol

molarity_base = 2  #mol/L_base_dis

V_base_dis = 3 #L_base_dis

T = 25

T_units = 'celsius'

P = 10 

P_units = 'atm'

density_dis_estimated = 1000 #g/L

n_acid_array = numpy.linspace(0.01 ,100, steps) #Acid dis volume samples

pH_array = numpy.zeros(steps)

fraction_CO2 = numpy.zeros(steps)

fraction_hydrogencarbonate = numpy.zeros(steps)

fraction_carbonate = numpy.zeros(steps)

#Iterations

for i in range(steps):

#Calculations
    
    n_acid = n_acid_array[i]
    
    n_base = molarity_base * V_base_dis #mol_base
    
    m_base_dis = density_dis_estimated * V_base_dis #g_base_dis
    
    m_water_base = m_base_dis - MW_base * V_base_dis #g_water
    
        
    #Initialize a thermodynamic database
    
    db = Database('supcrt98.xml')
    
    
    #Define the chemical system
    
    editor = ChemicalEditor(db)
    
    editor.addAqueousPhase("CO2(aq) HCO3- CO3-- NH4+ H+ OH- H2O(l)")
    
    editor.addGaseousPhase("H2O(g) CO2(g) NH3(g)")
    
    
    #Construct the chemical system
    
    system = ChemicalSystem(editor)
    
    
    # Define the chemical equilibrium problem
    
    problem = EquilibriumProblem(system)
    
    problem.setTemperature(T, T_units)
    
    problem.setPressure(P, P_units)
    
    problem.add('H2O(l)', m_water_base, 'g')
    
    problem.add('CO2(g)', n_acid, 'mol')
    
    problem.add('NH3(g)', n_base, 'mol')
    
    
    #Calculate the chemical equilibrium state
    
    state = equilibrate(problem)
    
    
    #Output the calculated chemical state to a file
    
    properties = state.properties()
    
    evaluate_pH = ChemicalProperty.pH(system)
    
    pH = evaluate_pH(properties)
    
    pH_array[i] =  pH.val
    
    data = { species.name(): state.speciesAmount(species.name()) for species in system.species() }
    
    data_formatted = pandas.DataFrame(list(data.items()))
    
    data_formatted = numpy.array(data_formatted)
    
    co2_selected = numpy.select(data_formatted[:,0] == 'CO2(aq)', data_formatted[:,1])

    hydrogencarbonate_selected = numpy.select(data_formatted[:,0] == 'HCO3-', data_formatted[:,1])
    
    carbonate_selected = numpy.select(data_formatted[:,0] == 'CO3--', data_formatted[:,1])
    
    total = co2_selected + hydrogencarbonate_selected +carbonate_selected
    
    fraction_CO2[i] = co2_selected / total
    
    fraction_hydrogencarbonate[i] = hydrogencarbonate_selected / total

    fraction_carbonate[i] = carbonate_selected / total
    
plt.figure(1)

label = 'Alkalinity curves,  NH3+CO2 neutralization'

plt.plot(pH_array, fraction_CO2 , 'b-',  pH_array, fraction_hydrogencarbonate , 'g:' , pH_array, fraction_carbonate , 'ro')

plt.legend(['CO2','HCO3-', 'CO3--'])

plt.xlabel('pH, as a result of modifying CO2 loading')

plt.ylabel('fraction of inorganic Carbon specie')

plt.title(label)

plt.savefig(label + '.png')
