#Author-Fabian Schurig
#Description-

# Simple Add-In imports
import adsk.core, adsk.fusion, adsk.cam, traceback, os, gettext
# math imports
import math

'''
QAT = Quick Access Toolbar
define commandIds and inputIds
'''
commandIdOnQAT = 'createScrewCommandOnQAT'
commandIdOnPanel = 'createScrewCommandOnPanel'
selectionInputId = 'selectionInput'
distanceInputId = 'distanceValueCommandInput'
panelId = 'SolidCreatePanel'

'''
define default parameters to initialize the screw
'''
defaultCylinderheadScrewName= 'Screw'
defaultCylinderheadDiameter = 0.55
defaultCylinderheadHeight = 0.3
defaultHexagonDiameter = 0.25
defaultHexagonHeight = 0.19
defaultThreadLength = 0.8
defaultBodyLength = 1.0
defaultBodyDiameter = 0.25
defaultFilletRadius = 0.025
defaultChamferDistance = 0.025


# global set of event handlers to keep them referenced for the duration of the command
handlers = []
app = adsk.core.Application.get()
if app:
    ui = app.userInterface

newComp = None

'''
function createNewComponent
This function gets the current design of the user and creates a new component in it.
returns a new component in the current design
'''
def createNewComponent():
    # Get the active design.
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    rootComp = design.rootComponent
    allOccs = rootComp.occurrences
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
    return newOcc.component

'''
Support localization
function getUserLanguage
returns the users language
'''
_ = None
def getUserLanguage():
    app = adsk.core.Application.get()
    
    return {
        adsk.core.UserLanguages.ChinesePRCLanguage: "zh-CN",
        adsk.core.UserLanguages.ChineseTaiwanLanguage: "zh-TW",
        adsk.core.UserLanguages.CzechLanguage: "cs-CZ",
        adsk.core.UserLanguages.EnglishLanguage: "en-US",
        adsk.core.UserLanguages.FrenchLanguage: "fr-FR",
        adsk.core.UserLanguages.GermanLanguage: "de-DE",
        adsk.core.UserLanguages.HungarianLanguage: "hu-HU",
        adsk.core.UserLanguages.ItalianLanguage: "it-IT",
        adsk.core.UserLanguages.JapaneseLanguage: "ja-JP",
        adsk.core.UserLanguages.KoreanLanguage: "ko-KR",
        adsk.core.UserLanguages.PolishLanguage: "pl-PL",
        adsk.core.UserLanguages.PortugueseBrazilianLanguage: "pt-BR",
        adsk.core.UserLanguages.RussianLanguage: "ru-RU",
        adsk.core.UserLanguages.SpanishLanguage: "es-ES"
    }[app.preferences.generalPreferences.userLanguage]

'''
Get loc string by language
'''
def getLocStrings():
    currentDir = os.path.dirname(os.path.realpath(__file__))
    return gettext.translation('resource', currentDir, [getUserLanguage(), "en-US"]).gettext 

'''

'''
def commandDefinitionById(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox(_('commandDefinition id is not specified'))
        return None
    commandDefinitions_ = ui.commandDefinitions
    commandDefinition_ = commandDefinitions_.itemById(id)
    return commandDefinition_

'''

'''
def commandControlByIdForQAT(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox(_('commandControl id is not specified'))
        return None
    toolbars_ = ui.toolbars
    toolbarQAT_ = toolbars_.itemById('QAT')
    toolbarControls_ = toolbarQAT_.controls
    toolbarControl_ = toolbarControls_.itemById(id)
    return toolbarControl_

'''

'''
def commandControlByIdForPanel(id):
    app = adsk.core.Application.get()
    ui = app.userInterface
    if not id:
        ui.messageBox(_('commandControl id is not specified'))
        return None
    workspaces_ = ui.workspaces
    modelingWorkspace_ = workspaces_.itemById('FusionSolidEnvironment')
    toolbarPanels_ = modelingWorkspace_.toolbarPanels
    toolbarPanel_ = toolbarPanels_.itemById(panelId)
    toolbarControls_ = toolbarPanel_.controls
    toolbarControl_ = toolbarControls_.itemById(id)
    return toolbarControl_

'''

'''
def destroyObject(uiObj, tobeDeleteObj):
    if uiObj and tobeDeleteObj:
        if tobeDeleteObj.isValid:
            tobeDeleteObj.deleteMe()
        else:
            uiObj.messageBox(_('tobeDeleteObj is not a valid object'))

'''
class Screw
'''
class Screw:
    def __init__(self):
        self._screwName = defaultCylinderheadScrewName
        self._headDiameter = adsk.core.ValueInput.createByReal(defaultCylinderheadDiameter)
        self._bodyDiameter = adsk.core.ValueInput.createByReal(defaultBodyDiameter)
        self._headHeight = defaultCylinderheadHeight
        self._bodyLength = adsk.core.ValueInput.createByReal(defaultBodyLength)
        self._hexagonDiameter = adsk.core.ValueInput.createByReal(defaultHexagonDiameter)
        self._hexagonHeight = adsk.core.ValueInput.createByReal(defaultHexagonHeight)
        self._filletRadius = adsk.core.ValueInput.createByReal(defaultFilletRadius)
        self._threadLength = adsk.core.ValueInput.createByReal(defaultThreadLength)
        self._chamferDistance = defaultChamferDistance

    #properties
    @property
    def screwName(self):
        return self._screwName
    @screwName.setter
    def screwName(self, value):
        self._screwName = value

    @property
    def headDiameter(self):
        return self._headDiameter
    @headDiameter.setter
    def headDiameter(self, value):
        self._headDiameter = value

    @property
    def bodyDiameter(self):
        return self._bodyDiameter
    @bodyDiameter.setter
    def bodyDiameter(self, value):
        self._bodyDiameter = value 

    @property
    def headHeight(self):
        return self._headHeight
    @headHeight.setter
    def headHeight(self, value):
        self._headHeight = value 

    @property
    def bodyLength(self):
        return self._bodyLength
    @bodyLength.setter
    def bodyLength(self, value):
        self._bodyLength = value   

    @property
    def threadLength(self):
        return self._threadLength
    @threadLength.setter
    def threadLength(self, value):
        self._threadLength = value  

    @property
    def hexagonDiameter(self):
        return self._hexagonDiameter
    @hexagonDiameter.setter
    def hexagonDiameter(self, value):
        self._hexagonDiameter = value

    @property
    def hexagonHeight(self):
        return self._hexagonHeight
    @hexagonHeight.setter
    def hexagonHeight(self, value):
        self._hexagonHeight = value
        
    @property
    def filletRadius(self):
        return self._filletRadius
    @filletRadius.setter
    def filletRadius(self, value):
        self._filletRadius = value
    
    @property
    def chamferDistance(self):
        return self._chamferDistance
    @chamferDistance.setter
    def chamferDistance(self, value):
        self._chamferDistance = value

    def buildScrew(self):
        global newComp
        newComp = createNewComponent()
        if newComp is None:
            ui.messageBox('New component failed to create', 'New Component Failed')
            return

        # Create a new sketch.
        sketches = newComp.sketches
        xyPlane = newComp.xYConstructionPlane
        xzPlane = newComp.xZConstructionPlane
        sketch = sketches.add(xyPlane)
        center = adsk.core.Point3D.create(0, 0, 0)
        sketch.sketchCurves.sketchCircles.addByCenterRadius(center, self.headDiameter/2)

        extrudes = newComp.features.extrudeFeatures
        prof = sketch.profiles[0]
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        distance = adsk.core.ValueInput.createByReal(self.headHeight)
        extInput.setDistanceExtent(False, distance)
        headExt = extrudes.add(extInput)

        fc = headExt.faces[0]
        bd = fc.body
        bd.name = self.screwName
        
        # Get construction planes
        planes = newComp.constructionPlanes
        
        # Create construction plane input
        planeInput = planes.createInput()
        
        # Add construction plane by offset
        offsetValue = adsk.core.ValueInput.createByReal(self.headHeight)
        planeInput.setByOffset(xyPlane, offsetValue)
        planeOne = planes.add(planeInput)
        
        #cut the hexagon
        sketchHex = sketches.add(xyPlane)
        vertices = []
        hexagonOuterDiameter = self.hexagonDiameter/math.sqrt(3)
        for i in range(0, 6):
            vertex = adsk.core.Point3D.create(center.x + (hexagonOuterDiameter) * math.cos(math.pi * i / 3), center.y + (hexagonOuterDiameter) * math.sin(math.pi * i / 3),0)
            vertices.append(vertex)

        for i in range(0, 6):
            sketchHex.sketchCurves.sketchLines.addByTwoPoints(vertices[(i+1) %6], vertices[i])

        extrudes = newComp.features.extrudeFeatures
        prof = sketchHex.profiles[0]
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)

        distance = adsk.core.ValueInput.createByReal(self.hexagonHeight)
        extInput.setDistanceExtent(False, distance)
        hexExt = extrudes.add(extInput)

        fc = hexExt.faces[0]
        bd = fc.body
        bd.name = self.screwName

        #create the body
        bodySketch = sketches.add(planeOne)
        bodySketch.sketchCurves.sketchCircles.addByCenterRadius(center, self.bodyDiameter/2)

        bodyProf = bodySketch.profiles[0]
        bodyExtInput = extrudes.createInput(bodyProf, adsk.fusion.FeatureOperations.JoinFeatureOperation)

        bodyExtInput.setAllExtent(adsk.fusion.ExtentDirections.NegativeExtentDirection)
        bodyExtInput.setDistanceExtent(False, self.bodyLength)
        bodyExt = extrudes.add(bodyExtInput)

        # create chamfer
        edgeCol = adsk.core.ObjectCollection.create()
        edges = bodyExt.endFaces[0].edges
        for edgeI  in edges:
            edgeCol.add(edgeI)

        chamferFeats = newComp.features.chamferFeatures
        chamferInput = chamferFeats.createInput(edgeCol, True)
        chamferInput.setToEqualDistance(self.chamferDistance)
        chamferFeats.add(chamferInput)
        
        # create fillet
        edgeCol.clear()
        facesLoop = headExt.faces
        for face in facesLoop:
            loops = face.loops
            edgeLoop = None
            for edgeLoop in loops:
                if(len(edgeLoop.edges) == 1):
                    edgeCol.add(edgeLoop.edges[0])
                    break
        
        #edgeCol.add(headExt.faces[0].loops[0].edges[0])
        #edgeCol.add(headExt.faces[0].loops[1].edges[0])
        #edgeCol.add(headExt.endFaces[0].loops[0].edges[0])
        
        filletFeats = newComp.features.filletFeatures
        filletInput = filletFeats.createInput()
        filletInput.addConstantRadiusEdgeSet(edgeCol, self.filletRadius, True)
        filletFeats.add(filletInput)
        
        #create thread
        sideFace = bodyExt.sideFaces[0]
        threads = newComp.features.threadFeatures
        threadDataQuery = threads.threadDataQuery
        defaultThreadType = threadDataQuery.defaultMetricThreadType
        recommendData = threadDataQuery.recommendThreadData(self.bodyDiameter, False, defaultThreadType)
        if recommendData[0] :
            threadInfo = threads.createThreadInfo(False, defaultThreadType, recommendData[1], recommendData[2])
            faces = adsk.core.ObjectCollection.create()
            faces.add(sideFace)
            threadInput = threads.createInput(faces, threadInfo)
            threadInput.isFullLength = False
            threadInput.threadLength = adsk.core.ValueInput.createByReal(self.threadLength)
            threads.add(threadInput)
    
'''
run - main function of the Add-in
'''       
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        global _
        _ = getLocStrings()
        
        commandName = _('Create Screw')
        commandDescription = _('Create a Screw by set of different parameters')
        commandResources = './resources'
        iconResources = './resources'
        
        screw = Screw()

        '''
        function InputChangedHandler triggers if sth was changed
        '''
        class InputChangedHandler(adsk.core.InputChangedEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    command = args.firingEvent.sender
                except:
                    if ui:
                        ui.messageBox(_('Input changed event failed: {}').format(traceback.format_exc()))

        class CommandExecuteHandler(adsk.core.CommandEventHandler):
            def __init__(self):
                super().__init__()
            def notify(self, args):
                try:
                    unitsMgr = app.activeProduct.unitsManager
                    command = args.firingEvent.sender
                    inputs = command.commandInputs
                    defaultUnits = unitsMgr.defaultLengthUnits
                    
                    
                    for input in inputs:
                        if input.id == 'screwName':
                            screw.screwName = input.value
                        elif input.id == 'headDiameter':
                            screw.headDiameter = unitsMgr.evaluateExpression(input.expression, "mm")
                        elif input.id == 'bodyDiameter':
                            screw.bodyDiameter = unitsMgr.evaluateExpression(input.expression, "mm")
                        elif input.id == 'headHeight':
                            screw.headHeight = unitsMgr.evaluateExpression(input.expression, "mm")
                        elif input.id == 'bodyLength':
                            screw.bodyLength = adsk.core.ValueInput.createByString(input.expression)
                        elif input.id == 'filletRadius':
                            screw.filletRadius = adsk.core.ValueInput.createByString(input.expression)
                        elif input.id == 'threadLength':
                            screw.threadLength = unitsMgr.evaluateExpression(input.expression, "mm")
                        elif input.id == 'hexagonDiameter':
                            screw.hexagonDiameter = unitsMgr.evaluateExpression(input.expression, "mm")
                        elif input.id == 'hexagonHeight':
                            screw.hexagonHeight = unitsMgr.evaluateExpression(input.expression, "mm")
                        elif input.id == 'chamferDistance':
                            screw.chamferDistance = adsk.core.ValueInput.createByString(input.expression)
                        
                    screw.buildScrew();
                    args.isValidResult = True
                    ui.messageBox(_('command: {} executed successfully').format(command.parentCommandDefinition.id))
                except:
                    if ui:
                        ui.messageBox(_('command executed failed: {}').format(traceback.format_exc()))

        class CommandCreatedEventHandlerPanel(adsk.core.CommandCreatedEventHandler):
            def __init__(self):
                super().__init__() 
            def notify(self, args):
                try:
                    cmd = args.command
                    cmd.isRepeatable = False
                    cmd.helpFile = 'help.html'
                    
                    onExecute = CommandExecuteHandler()
                    cmd.execute.add(onExecute)

                    onInputChanged = InputChangedHandler()
                    cmd.inputChanged.add(onInputChanged)
                    # keep the handler referenced beyond this function
                    handlers.append(onExecute)
                    handlers.append(onInputChanged)

                    #define the inputs
                    inputs = cmd.commandInputs
                    inputs.addStringValueInput('screwName', _('Screw Name'), defaultCylinderheadScrewName)

                    initHeadDiameter = adsk.core.ValueInput.createByReal(defaultCylinderheadDiameter)
                    inputs.addValueInput('headDiameter', _('Head Diameter'),'mm', initHeadDiameter)

                    initBodyDiameter = adsk.core.ValueInput.createByReal(defaultBodyDiameter)
                    inputs.addValueInput('bodyDiameter', _('Body Diameter'), 'mm', initBodyDiameter)

                    initHeadHeight = adsk.core.ValueInput.createByReal(defaultCylinderheadHeight)
                    inputs.addValueInput('headHeight', _('Head Height'), 'mm', initHeadHeight)

                    initBodyLength = adsk.core.ValueInput.createByReal(defaultBodyLength)
                    inputs.addValueInput('bodyLength', _('Body Length'), 'mm', initBodyLength)
                    
                    initHexagonDiameter = adsk.core.ValueInput.createByReal(defaultHexagonDiameter)
                    inputs.addValueInput('hexagonDiameter', _('Hexagon Diameter'), 'mm', initHexagonDiameter)
                    
                    initHexagonHeight = adsk.core.ValueInput.createByReal(defaultHexagonHeight)
                    inputs.addValueInput('hexagonHeight', _('Hexagon Height'), 'mm', initHexagonHeight)

                    #to do the thread length

                    initFilletRadius = adsk.core.ValueInput.createByReal(defaultFilletRadius)
                    inputs.addValueInput('filletRadius', _('Fillet Radius'), 'mm', initFilletRadius)
                    
                    initThreadLength = adsk.core.ValueInput.createByReal(defaultThreadLength)
                    inputs.addValueInput('threadLength', _('Thread Length'), 'mm', initThreadLength)
                    
                    initChamferDistance = adsk.core.ValueInput.createByReal(defaultChamferDistance)
                    inputs.addValueInput('chamferDistance', _('Chamfer Distance'), 'mm', initChamferDistance)
                    

                    '''
                    selInput = commandInputs_.addSelectionInput(selectionInputId, _('Selection'), _('Select one'))
                    selInput.addSelectionFilter('PlanarFaces')
                    selInput.addSelectionFilter('ConstructionPlanes')
                    dropDownCommandInput_ = commandInputs_.addDropDownCommandInput('dropdownCommandInput', _('Drop Down'), adsk.core.DropDownStyles.LabeledIconDropDownStyle)
                    dropDownItems_ = dropDownCommandInput_.listItems
                    dropDownItems_.add(_('ListItem 1'), True)
                    dropDownItems_.add(_('ListItem 2'), False)
                    dropDownItems_.add(_('ListItem 3'), False)
                    '''
                    
                    ui.messageBox(_('Panel command created successfully'))
                except:
                    if ui:
                        ui.messageBox(_('Panel command created failed: {}').format(traceback.format_exc()))

        commandDefinitions_ = ui.commandDefinitions
        
        # add a command on create panel in modeling workspace
        workspaces_ = ui.workspaces
        modelingWorkspace_ = workspaces_.itemById('FusionSolidEnvironment')
        toolbarPanels_ = modelingWorkspace_.toolbarPanels
        toolbarPanel_ = toolbarPanels_.itemById(panelId) # add the new command under the CREATE panel
        toolbarControlsPanel_ = toolbarPanel_.controls
        toolbarControlPanel_ = toolbarControlsPanel_.itemById(commandIdOnPanel)
        if not toolbarControlPanel_:
            commandDefinitionPanel_ = commandDefinitions_.itemById(commandIdOnPanel)
            if not commandDefinitionPanel_:
                commandDefinitionPanel_ = commandDefinitions_.addButtonDefinition(commandIdOnPanel, commandName, commandDescription, commandResources)
                commandDefinitionPanel_.toolClipFilename = './resources/medium.png'
            onCommandCreated = CommandCreatedEventHandlerPanel()
            commandDefinitionPanel_.commandCreated.add(onCommandCreated)
            # keep the handler referenced beyond this function
            handlers.append(onCommandCreated)
            toolbarControlPanel_ = toolbarControlsPanel_.addCommand(commandDefinitionPanel_)
            toolbarControlPanel_.isVisible = True
            ui.messageBox(_('The command is successfully added to the create panel in modeling workspace'))

    except:
        if ui:
            ui.messageBox(_('AddIn Start Failed: {}').format(traceback.format_exc()))
            
            
            
'''
Stop function runs when Add-In is stopped or Fusion crashes
'''            
def stop(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        objArrayQAT = []
        objArrayPanel = []

        commandControlQAT_ = commandControlByIdForQAT(commandIdOnQAT)
        if commandControlQAT_:
            objArrayQAT.append(commandControlQAT_)

        commandDefinitionQAT_ = commandDefinitionById(commandIdOnQAT)
        if commandDefinitionQAT_:
            objArrayQAT.append(commandDefinitionQAT_)

        commandControlPanel_ = commandControlByIdForPanel(commandIdOnPanel)
        if commandControlPanel_:
            objArrayPanel.append(commandControlPanel_)

        commandDefinitionPanel_ = commandDefinitionById(commandIdOnPanel)
        if commandDefinitionPanel_:
            objArrayPanel.append(commandDefinitionPanel_)

        for obj in objArrayQAT:
            destroyObject(ui, obj)

        for obj in objArrayPanel:
            destroyObject(ui, obj)
        ui.messageBox(_('Addin succesfully stopped!'))
    except:
        if ui:
            ui.messageBox(_('AddIn Stop Failed: {}').format(traceback.format_exc()))