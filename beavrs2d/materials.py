from generatehdf5 import generate
import openmoc.materialize as materialize


assembly_names = ['pwru160c00','pwru240c00','pwru240w12', 'pwru240w16', 'pwru310c00', 'pwru310w06', 'pwru310w12', 'pwru310w15', 'pwru310w16', 'pwru310w20']
group_types = ['2-group/','8-group/']

# generate hdf5 files
generate(assembly_names, group_types)

group_names =['2','8']
materials = {}

# create materials for each assembly and number of groups
for group in group_names:
  materials[group] = {}
  for name in assembly_names:
    materials[group][name] = materialize.materialize('casmo-data/'+ group + '-group/' + name + '-avg-materials.hdf5')

