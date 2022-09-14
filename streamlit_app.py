# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:50:04 2022

@author: ENRIQUE
"""

import reaktoro as rkt
from reaktoro import *
import streamlit as st
import pandas as pd


# -- Set page config
apptitle = 'Streamlit debugging'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

# Title the app
st.title(apptitle)

st.markdown("""
 * Use the menu at left to select data and set plot parameters
 * Your plots will appear below
""")



Water = pd.DataFrame(index = ['Ca+2','Mg+2','Na+','Cl-','NO3-','SO4-2'], columns=["loading", "wt_fraction_dry"])

Water.loc["Ca+2" ,  "loading"]   =  102  #mg/L
Water.loc["Mg+2",   "loading"]   =  8.81 #mg/L
Water.loc["Na+" ,   "loading"]   =  49.1 #mg/L
Water.loc["Cl-",    "loading"]   =  73.9 #mg/L
Water.loc["NO3-",   "loading"]   =  20.6 #mg/L
Water.loc["SO4-2",  "loading"]   =  120  #mg/L

Water.wt_fraction_dry = (Water['loading'] / Water['loading'].sum())

TDS = 550 #mg/kg
mass = 1 #kg

st.markdown(print("An inflow of brackish water enters a Reverse Osmosis Unit"))
st.markdown(print("With a Total Dissolved Solids (TDS) of", TDS, "mg/kg"))



#Initialize a thermodynamic database
 

db = SupcrtDatabase("supcrtbl")

#Define the chemical system

species = ("H2O(aq) H+ OH- Na+ Cl- Ca+2 Mg+2 NO3- SO4-2")
species_list = species.split()

solution = AqueousPhase(species)

solution.setActivityModel(ActivityModelHKF())

system = ChemicalSystem(db, solution)

state = ChemicalState(system)
state.temperature(25, "C")
state.pressure(1, "atm")
state.set("H2O(aq)", mass * (1e6 - TDS)/1e6 , "kg")

for ion, row in Water.iterrows():
  state.set(ion, Water.loc[ion, "wt_fraction_dry"] * mass * TDS/1e6,   "kg")

solver = EquilibriumSolver(system)

result = solver.solve(state)  # equilibrate the `state` object!
assert result.optima.succeeded


st.markdown(print(state))    