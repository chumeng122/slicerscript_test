import slicer
import vtk
# merge subfields of hippocampal 
# input: segment node / volume node  
# output: union of segment name  
def merge_seg(segNode,volNode):
    # Create segment editor to get access to effects
    segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    segmentEditorWidget.show() # To show segment editor widget (useful for debugging)
    segmentEditorWidget.setMRMLScene(slicer.mrmlScene)

    # set up segmentation and source volume
    segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode") #//
    segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)

    segmentEditorWidget.setSegmentationNode(segNode)
    segmentEditorWidget.setSourceVolumeNode(volNode)
   
    # create a empty segment
    segment_id = segNode.GetSegmentation().AddEmptySegment() # create a new segment

    # choose
    segmentEditorNode.SetSelectedSegmentID(segment_id) #//
    segmentEditorNode.SetMaskMode(2)
    segmentEditorNode.SetOverwriteMode(2)
    # edible area 修改方式: segmentEditorNode.SetMaskMode(1) 改數字
    # modify mask: segmentEditorNode.SetOverwriteMode(0)

    # call segmentation editor option
    # setpara ways: https://slicer.readthedocs.io/en/latest/developer_guide/modules/segmenteditor.html#logical-operators
    segmentEditorWidget.setActiveEffectByName("Logical operators")
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("Operation", "FILL")
    effect.setParameter("BypassMasking",0)
    effect.setParameter("ModifierSegmentID",segment_id) # choose
    effect.self().onApply()
    
    segmentEditorWidget.close()
    return segment_id

# close visibility of segments except "newsegid" 
# input: segNode, segment id ("newsegid")
def onlyvisible(segNode,newsegid):
    if segNode:
        display = segNode.GetDisplayNode()
        segmentation = segNode.GetSegmentation()
        for segmentIndex in range(segmentation.GetNumberOfSegments()):
            display.SetSegmentVisibility(segmentation.GetNthSegmentID(segmentIndex), False)
        
        nid = segmentation.GetSegmentIndex(newsegid)
        display.SetSegmentVisibility(segmentation.GetNthSegmentID(nid), True)
        return True
    print("may be sth not exist")
    return False

# export visible segment (in segNode) to model (in "newf")
# input: segNode / foldername(str)
# output: modelNode  
# if anything wrong return segNode
def seg2modelNode(segNode,foldername):
    shNode = slicer.mrmlScene.GetSubjectHierarchyNode() 
    folderItemID = shNode.CreateFolderItem(shNode.GetSceneItemID(), foldername)
    slicer.modules.segmentations.logic().ExportVisibleSegmentsToModels(segNode,folderItemID)
    childIds = vtk.vtkIdList()
    #sceneItemID = shNode.GetSceneItemID()
    #shFolderItemId = shNode.GetItemChildWithName(sceneItemID, "F")
    #shNode.GetItemChildren(shFolderItemId, childIds)
    shNode.GetItemChildren(folderItemID, childIds) 
    if childIds.GetNumberOfIds() == 1:
        cid = childIds.GetId(0)
        childNode = slicer.mrmlScene.GetSubjectHierarchyNode().GetItemDataNode(cid)
    else:
        print("folder has more than one ids")
        return segNode
    return childNode

# set multiple segments to be invisible except alist
# input: segNode / assign visible segment (list)
def list_visible(segNode,seg_vis):
    couname = len(seg_vis)
    display = segNode.GetDisplayNode()
    segmentation = segNode.GetSegmentation()
    for segmentIndex in range(segmentation.GetNumberOfSegments()):
        tmpname = segmentation.GetNthSegment(segmentIndex).GetName()
        if tmpname in seg_vis:
            display.SetSegmentVisibility(segmentation.GetNthSegmentID(segmentIndex), True)  
            couname = couname - 1
        else:
            display.SetSegmentVisibility(segmentation.GetNthSegmentID(segmentIndex), False)  
    if not couname == 0:
        print("not all seg visiable in seg_vis")
        return False
    return True    

# smooth a segment by filling hole with smoo_pt mm then median smooth filiter with smoo_pt mm
# input: segNode / volNode / assign segment to fill / smooth kernel size mm
# output: assign segment to fill (finish smoothing)
# All segments except the input one will be set invisible 
def smmoooth(segNode,volNode,newsegid,smoo_pt1):
    # Create segment editor to get access to effects
    segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    segmentEditorWidget.show() # To show segment editor widget (useful for debugging)
    segmentEditorWidget.setMRMLScene(slicer.mrmlScene)

    # set up segmentation and source volume
    segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode") #//
    segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)

    segmentEditorWidget.setSegmentationNode(segNode)
    segmentEditorWidget.setSourceVolumeNode(volNode)
    onlyvisible(segNode,newsegid)
    # choose
    segmentEditorNode.SetSelectedSegmentID(newsegid) #//
    # edible area 修改方式: segmentEditorNode.SetMaskMode(1) 改數字
    # modify mask: segmentEditorNode.SetOverwriteMode(0)
    segmentEditorNode.SetMaskMode(0)
    segmentEditorNode.SetOverwriteMode(2)

    # call segmentation editor option
    # setpara ways: https://slicer.readthedocs.io/en/latest/developer_guide/modules/segmenteditor.html#logical-operators
    segmentEditorWidget.setActiveEffectByName("Smoothing")
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("ApplyToAllVisibleSegments", 0)
    effect.setParameter("SmoothingMethod","MORPHOLOGICAL_CLOSING")
    effect.setParameter("KernelSizeMm",smoo_pt1)
    effect.self().onApply()
    
    # segmentEditorWidget.setActiveEffectByName("Smoothing")
    # effect = segmentEditorWidget.activeEffect()
    # effect.setParameter("ApplyToAllVisibleSegments", 0)
    # effect.setParameter("SmoothingMethod","MEDIAN")
    # effect.setParameter("KernelSizeMm",smoo_pt2)
    # effect.self().onApply()
    
    segmentEditorWidget.close()
    return newsegid

