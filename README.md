# slicerscript_test

Description:
[3D Slicer](https://slicer.readthedocs.io/en/latest/developer_guide/api.html) <\br>
處理[Freesurfer](https://surfer.nmr.mgh.harvard.edu)海馬迴亞區分割("Segment_226","Segment_231","Segment_232")的合併與平滑化。

## usage
資料放在：
\datafolder\raw\a\orig  MRI圖像(.nii.gz)
\datafolder\seg\a\lh    亞區分割後的(.nii.gz)

Before using:
`
1. open slicer3d && python console
2. type below: Set up python workspace
      import os
      os.chdir("(path to)/slicerscript_test") 
3. Have you already set up path of "some_tool"?
      import sys
      sys.path.append((path to your "slicerscript_test"))
      Example: sys.path.append(os.getcwd())
4. exec(open("with_smooth.py").read())  
`