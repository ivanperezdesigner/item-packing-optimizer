' ******************************************************************************
' C:\Users\IvanPerez\AppData\Local\Temp\swx36068\Macro1.swb - macro recorded on 05/11/26 by IvanPerez
' ******************************************************************************
Dim swApp As Object

Dim Part As Object
Dim boolstatus As Boolean
Dim longstatus As Long, longwarnings As Long

Sub main()

Set swApp = Application.SldWorks


' New Document
Dim swSheetWidth As Double
swSheetWidth = 0
Dim swSheetHeight As Double
swSheetHeight = 0
Set Part = swApp.NewDocument("C:\ProgramData\SolidWorks\SOLIDWORKS 2024\templates\Assembly.asmdot", 0, swSheetWidth, swSheetHeight)
Dim swAssembly As AssemblyDoc
Set swAssembly = Part
swApp.ActivateDoc2 "Assem2", False, longstatus
Set Part = swApp.ActiveDoc

' Take Snapshot
Dim swSnapShot As SnapShot
Set swSnapShot = Part.ModelViewManager.AddSnapShot("Home")
Dim myModelView As Object
Set myModelView = Part.ActiveView
myModelView.FrameState = swWindowState_e.swWindowMaximized
boolstatus = Part.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, Nothing, 0)
Part.SketchManager.InsertSketch True
Dim skPoint As Object
Set skPoint = Part.SketchManager.CreatePoint(0#, 0#, 0#)
Set skPoint = Part.SketchManager.CreatePoint(0.023261, 0#, 0#)

' Zoom In/Out (MouseWheel)
Dim swModelView As Object
Set swModelView = Part.ActiveView
swModelView.Scale2 = 1.15062159465889
Dim swTranslation() As Double
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 2.65464453733301E-02
swTranslation(1) = 1.8712748955003E-04
swTranslation(2) = 0
Dim swTranslationVar As Variant
swTranslationVar = swTranslation
Dim swMathUtils As Object
Set swMathUtils = swApp.GetMathUtility()
Dim swTranslationVector As MathVector
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 1.38629107790228
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 3.35355443806206E-02
swTranslation(1) = 3.65800423849324E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 1.67023021434009
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 4.19561455942237E-02
swTranslation(1) = 5.81069019390629E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 2.0123255594459
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 5.21014482612153E-02
swTranslation(1) = 8.40428773054851E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 2.42448862583843
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 6.43247044865064E-02
swTranslation(1) = 1.15291040397559E-03
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 2.02040718819869
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 5.70615026049685E-02
swTranslation(1) = 9.60758669979671E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 1.68367265683224
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 5.10088343703535E-02
swTranslation(1) = 8.00632224983056E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 1.4030605473602
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 4.59649441748411E-02
swTranslation(1) = 6.67193520819217E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 1.16921712280017
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 4.17617023452474E-02
swTranslation(1) = 5.5599460068267E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.974347602333474
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 0.038259000820586
swTranslation(1) = 4.63328833902229E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.811956335277895
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 3.53400828833682E-02
swTranslation(1) = 3.86107361585184E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.676630279398246
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 3.29076512690199E-02
swTranslation(1) = 3.2175613465433E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.563858566165205
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 3.08806249237298E-02
swTranslation(1) = 2.68130112211942E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.469882138471004
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 2.91914363026546E-02
swTranslation(1) = 2.23441760176615E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.391568448725837
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 2.77837791184253E-02
swTranslation(1) = 1.86201466813842E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.326307040604864
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 2.66107314649009E-02
swTranslation(1) = 1.55167889011532E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector
Set skPoint = Part.SketchManager.CreatePoint(0.332541, 0#, 0#)

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.271922533837387
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 2.56331917536306E-02
swTranslation(1) = 1.29306574176283E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.226602111531156
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 0.024818575327572
swTranslation(1) = 1.07755478480233E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.18883509294263
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 2.41397283058565E-02
swTranslation(1) = 8.97962320668535E-05
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.157362577452191
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = 2.35740224544269E-02
swTranslation(1) = 7.48301933890481E-05
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector
Set skPoint = Part.SketchManager.CreatePoint(0.764853, 0#, 0#)

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.189593466809869
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = -1.41142118408266E-02
swTranslation(1) = 1.36938731892388E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.228425863626348
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = -5.95217230399271E-02
swTranslation(1) = 2.11768296354244E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.275211883887167
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = -0.114229567858121
swTranslation(1) = 3.01924398115524E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.331580582996586
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = -0.180142633904137
swTranslation(1) = 4.10546207466445E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.276317152497155
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = -0.146661279387234
swTranslation(1) = 3.42121839555378E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.23026429374763
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = -0.118760150623149
swTranslation(1) = 2.85101532962811E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.191886911456358
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = -9.55092099864108E-02
swTranslation(1) = 2.37584610802336E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector

' Zoom In/Out (MouseWheel)
Set swModelView = Part.ActiveView
swModelView.Scale2 = 0.159905759546965
ReDim swTranslation(0 To 2) As Double
swTranslation(0) = -7.61334261224625E-02
swTranslation(1) = 1.97987175668617E-04
swTranslation(2) = 0
swTranslationVar = swTranslation
Set swMathUtils = swApp.GetMathUtility()
Set swTranslationVector = swMathUtils.CreateVector((swTranslationVar))
swModelView.Translation3 = swTranslationVector
Set skPoint = Part.SketchManager.CreatePoint(1.213197, 0#, 0#)
boolstatus = Part.EditRebuild3()
Part.ClearSelection2 True

' Save As
longstatus = Part.SaveAs3("C:\Users\IvanPerez\OneDrive - SACO Technologies Inc\Desktop\points.SLDASM", 0, 0)

' Close Document
Set swAssembly = Nothing
Set Part = Nothing
swApp.CloseDoc "points.SLDASM"
End Sub
