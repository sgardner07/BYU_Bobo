import hou
from pxr import Usd, Sdf

#ROP node
node = hou.pwd()

#Get the ROP node
rop_node = hou.pwd()

#Get the USD file from the ROP, open it as a USD stage
stage = rop_node.input(0).stage()

#Get stage root layer
root_layer = stage.GetRootLayer()

# ✅ Create a temporary in-memory layer for deactivation override
override_layer = Sdf.Layer.CreateAnonymous("deactivate_layer")

# Inject the override layer into the stage's root layer
if override_layer.identifier not in stage.GetRootLayer().subLayerPaths:
    stage.GetRootLayer().subLayerPaths.append(override_layer.identifier)

# Set it as the active edit target
stage.SetEditTarget(Usd.EditTarget(override_layer))

# Safely deactivate the static HairGen prim
hairgen_path = Sdf.Path("/environment/grass")
stage.OverridePrim(hairgen_path).SetActive(False)

#Get stage root layer
#root_layer = stage.GetRootLayer()

#Create temporary Houdini LOP Network
temp_lopnet = hou.node('/stage').createNode('lopnet', 'temp_procedural_net')

#Create HDA instance inside temporary lopnet
hda_node = temp_lopnet.createNode('sleister::modify_curves_prerender::1.0', 'modify_curves_prerender')


#Cook it to apply
hda_node.cook(force=True)

#Run a USD ROP to flatten layer
usd_rop = hda_node.node("usd_rop")
frame = int(hou.frame())
temp_usd_path = f"/tmp/hda_output_layer_{frame}.usda"
hda_node.parm("outputpath").set(temp_usd_path)

usd_rop.render()

    
#Inject this layer into the stage being rendered
if temp_usd_path not in root_layer.subLayerPaths:
    root_layer.subLayerPaths.append(temp_usd_path)

#Cleanup
temp_lopnet.destroy()

