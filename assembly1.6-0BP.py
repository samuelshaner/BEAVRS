from pincells import pincells
from lattices import lattices, pinPitch
from materials import materials
from openmoc import *
import openmoc.log as log
from surfaces import surfaces
import openmoc.plotter as plotter

#log.set_log_level('DEBUG')

groups = input('How many energy groups?')
if groups == '2' or groups == 2:
  group = '2'
elif groups == '8' or groups == 8:
  group = '8'

assembly = CellFill(universe=0, universe_fill= lattices[group]['1.6-0BP'].getId()) #create cell, fill with lattice


#create surfaces
left = openmoc.XPlane(x=-pinPitch*17/2.0)
right = openmoc.XPlane(x=pinPitch*17/2.0)
bottom = openmoc.YPlane(y=-pinPitch*17/2.0)
top = openmoc.YPlane(y=pinPitch*17/2.0)

#sets boundary condition to be reflective
left.setBoundaryType(REFLECTIVE)
right.setBoundaryType(REFLECTIVE)
bottom.setBoundaryType(REFLECTIVE)
top.setBoundaryType(REFLECTIVE)

#add surfaces to bound cell
assembly.addSurface(halfspace=+1, surface=left)
assembly.addSurface(halfspace=-1, surface=right)
assembly.addSurface(halfspace=+1, surface=bottom)
assembly.addSurface(halfspace=-1, surface=top)

geometry = Geometry() #initialize geometry

#add materials
materialtypes = ['fuel', 'cladding', 'helium', 'water']
for material in materialtypes:
  geometry.addMaterial(materials[group]['pwru160c00'][material])

#add surfaces
geometry.addSurface(left)
geometry.addSurface(right)
geometry.addSurface(bottom)
geometry.addSurface(top)

for surface in surfaces:
	geometry.addSurface(surfaces[surface])



#add ALL cells
geometry.addCell(pincells[group]['pwru160c00']['fuel'])
geometry.addCell(pincells[group]['pwru160c00']['cladding'])
geometry.addCell(pincells[group]['pwru160c00']['water'])
geometry.addCell(pincells[group]['pwru160c00']['helium'])
geometry.addCell(pincells[group]['pwru160c00']['guidetube']['water1'])
geometry.addCell(pincells[group]['pwru160c00']['guidetube']['water2'])
geometry.addCell(pincells[group]['pwru160c00']['guidetube']['cladding'])
geometry.addCell(pincells[group]['pwru160c00']['instube']['cladding1'])
geometry.addCell(pincells[group]['pwru160c00']['instube']['helium'])
geometry.addCell(pincells[group]['pwru160c00']['instube']['cladding2'])
geometry.addCell(pincells[group]['pwru160c00']['instube']['water1'])
geometry.addCell(pincells[group]['pwru160c00']['instube']['water2'])
geometry.addCell(assembly)

#add all lattices
geometry.addLattice(lattices[group]['1.6-0BP'])


#initialize flat source regions
geometry.initializeFlatSourceRegions()

#plot geometry by materials, cells, and FSRs
plotter.plot_cells(geometry)
plotter.plot_materials(geometry)
plotter.plot_flat_source_regions(geometry)

# Initialize the track generator after the geometry has been
# constructed. Use 64 azimuthal angles and 0.05 cm track spacing.
track_generator = openmoc.TrackGenerator(geometry, num_azim=64, \
                                         spacing=0.05)

# Generate tracks using ray tracing across the geometry
track_generator.generateTracks()

# Initialize a solver for the simulation and set the number of
# threads and source convergence threshold
solver = openmoc.ThreadPrivateSolver(geometry, track_generator)
solver.setNumThreads(4)
solver.setSourceConvergenceThreshold(1E-5)

# Converge the source with up to a maximum of 1000 source iterations
solver.convergeSource(1000)

# Print a report of the time to solution
solver.printTimerReport()

#Plot fluxes
plotter.plot_fluxes(geometry, solver)
