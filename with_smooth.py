# # usage
# before using
# 1. open slicer3d && python console
# 2. type below: Set up python workspace
#       import os
#       os.chdir("(path to)/slicerscript_test") 
# 3. Have you already set up path of "some_tool"?
#       import sys
#       sys.path.append((path to your "slicerscript_test"))
#       Example: sys.path.append(os.getcwd())
# 4. exec(open("with_smooth.py").read())  

from some_tool import mmerge  
import slicer
import glob
import os


## input foldername 
foldername = "a"

##
curp = os.getcwd()
raw_suffix = "orig_fspace.nii"
label_suffix = "_HBT_Lfsspa.nii.gz"
# label_suffix = "_HBT_Lfsspa.nrrd"
o_mesh_suffix = "_v74s3d_smoo.stl"

## create a output folder
if not os.path.exists(os.path.join(os.path.join(curp ,"datafolder","output", foldername))):
    os.makedirs(os.path.join(os.path.join(curp ,"datafolder","output", foldername,"hippseg")))
    
if not os.path.exists(os.path.join(os.path.join(curp ,"datafolder","output", foldername,"stlsmooo"))):
    os.makedirs(os.path.join(os.path.join(curp ,"datafolder","output", foldername,"stlsmooo")))

    
outputpath = os.path.join(os.path.join(curp ,"datafolder","output", foldername))
rawpath = os.path.join(curp ,"datafolder","raw", foldername, "orig")
lbpath = os.path.join(curp,"datafolder", "seg" , foldername , "lh")
rawfile = glob.glob(f'{rawpath}/*{raw_suffix}')

print(rawpath)
for i in range(len(rawfile)):
    rawdatapath = rawfile[i]
    rawname = os.path.basename(rawdatapath)
    labelname = rawname.replace(raw_suffix , label_suffix)
    labelpath = os.path.join(lbpath,labelname)
    
    # load file
    slicer.util.loadVolume(rawdatapath)
    slicer.util.loadSegmentation(labelpath)

    segNode = getNode(labelname) 
    volNode = getNode(rawname.strip(".nii.gz")) 

    seg_vis = ["Segment_226","Segment_231","Segment_232"]

    mmerge.list_visible(segNode,seg_vis)
    newsegid = mmerge.merge_seg(segNode,volNode)

    # # # let "newsegid" be the only visible segment in segNode
    mmerge.onlyvisible(segNode,newsegid)
    
    # # smooth
    mmerge.smmoooth(segNode,volNode,newsegid,3)
    
    
    # # export visible segment (in segNode) to model (in "newf") 
    modelNode = mmerge.seg2modelNode(segNode, "newf")

    # # export to binaey labelnode
    labelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode")
    slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(segNode, labelmapVolumeNode, volNode)
    
    # save node 
    slicer.util.saveNode(modelNode,os.path.join(outputpath, "stlsmooo", rawname.replace(raw_suffix, o_mesh_suffix)))
    slicer.util.saveNode(labelmapVolumeNode,os.path.join(outputpath, "hippseg", rawname.replace(raw_suffix,"_v74s3d_seg.nii.gz")))
     
    slicer.mrmlScene.Clear()