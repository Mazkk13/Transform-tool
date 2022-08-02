import maya.cmds as cmds
import math as m
from datetime import date
from functools import wraps
import re

'''
    ----------------------------------------------------------------
    script allows users to accurately control and 
    change transformation amounts of selected geometry
    by the application of trigonometric and arithmetic 
    operators.

    i.e
    translate sin(30) in x,y,z 
    translate 1+2 in x,y,z 
    translates selected geometry by sin(30) and 3 in relevant axes.

    user is able to specify whether the transformation should
    apply to local or global space. If global space is chosen, 
    then the selected geometry will transform based on the 
    global axis position of selected geometry. Otherwise, local space
    operations will affect the object's current location and apply 
    transformations upon the local positions of the object.
    -----------------------------------------------------------------
'''

def RuntimeErrorDecorator(fn):
    '''
        tries and excepts RuntimeErrors.
    '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except (RuntimeError):
            pass
    return wrapper
            
def isObjectSelected():
    '''
        detects whether any object exists in scene and is currenly selected.
        If such an object/objects exist in scene, return boolean statement.
    '''
    geometry = cmds.ls(geometry=True)
    if len(geometry)>0:
        selectedObjs = cmds.ls(selection=True)
        if len(selectedObjs)>0:
            return True            
        else:
            return False
    else:
        return False      
    
def evaluateExpressions(expressions, *args):
    '''
        evaluates the entered expression. If a trigonometric identity is 
        located within the expression, applies relevant function and returns
        value. Normal string expressions are evaluated and computed.
    '''
    trig_expressions = ['sin','cos','tan']
    correct_bracket_type, contains_trig_identities = False, False
    invalid_brackets = ['{','[',' ','_']
    for string in expressions:
        for bracket in invalid_brackets:
            if string in bracket:
                'invalid bracket type entered. Please try again'
                break
            else:
                'correct bracket type entered'
                correct_bracket_type = True  
        for trig_I in trig_expressions:
            if string in trig_I:
                contains_trig_identities=True
            else:
                break  
    try:
        if (correct_bracket_type is True) and (contains_trig_identities is True):
            number = re.findall('(?<=\()(.*?)(?=\))', expressions)
            operator = re.findall('(?<=\s)(.*?)(?=\s)', expressions)
            finalOp = []
            for i in operator:
                if len(i)<=1:
                    finalOp.append(i)
                else:
                    continue        
            trigIdentity = re.findall('[a-zA-Z]+', expressions)
            calculated_number = []
            for i in range(len(trigIdentity)):
                if trigIdentity[i]=='sin':
                    calculated_number.append(str(m.sin(float(number[i])))) 
                elif trigIdentity[i]=='cos':
                    calculated_number.append(str(m.cos(float(number[i]))))
                elif trigIdentity[i]=='tan':
                    calculated_number.append(str(m.tan(float(number[i]))))
            toEvaluate = [calculated_number[i] + finalOp[i] if i<=len(calculated_number)-2 
                            else calculated_number[i] for i in range(len(calculated_number))]
            compiler = ''
            for j in toEvaluate:
                compiler += j
            return eval(compiler)
        else:
            calculated_number = eval(expressions)
            return calculated_number
    except (ZeroDivisionError, SyntaxError, TypeError, ValueError):
       pass            
    
class UI:
    
    def __str__(self):
        display_info ='''
        
           --------------------------------------------------
           creates a UI to transform selected geometry
           by arithmetic amounts. There is also an option
           to apply trigonometric operators on selected 
           geometry to transform faces, edges, vertices and 
           vertex faces by specific amounts.
           
           i.e 
           Rotation = 20, 30, 40
           
           the operation above will rotate selected geometry 
           in corresponding axes by these amounts
           ---------------------------------------------------
           '''
        return display_info  
        
    def __init__(self, windowName='myWindow', shortName='myWin', *args):
        self.windowName = windowName
        self.shortName = shortName     
        self.isGlobal = False
        self.otherEntries = {}
    
    def detectType(self, *args):
        '''
            detect the geometry type and whether to translate based off existing position or not.
            if geometry type is global, transformations will be applied through the world position
            of selected geometry. Otherwise, transformations will apply to object space positions.
        '''
        queryGeometryType = cmds.checkBox(self.otherEntries['type'], query=True, value=True)
        if queryGeometryType:
            print('isGlobal')
            self.isGlobal = True
        else:
            print('isNotGlobal')
            self.isGlobal = False
    
    def appliesToGlobalComponent(self, objectSel, alias=None, **kwargs):
        '''
            applies the relevant component transformation to 
            selected geometry
        '''
        if alias=='vtx':
            cmds.polyMoveVertex(objectSel, translate=kwargs['translate'])
            cmds.polyMoveVertex(objectSel, rotate=kwargs['rotate'])
            cmds.polyMoveVertex(objectSel, scale=kwargs['scale'])
        elif alias=='e':
            cmds.polyMoveEdge(objectSel, translate=kwargs['translate'])
            cmds.polyMoveEdge(objectSel, rotate=kwargs['rotate'])
            cmds.polyMoveEdge(objectSel, scale=kwargs['scale'])
        elif alias=='f':
            cmds.polyMoveFacet(objectSel, translate=kwargs['translate'])
            cmds.polyMoveFacet(objectSel, rotate=kwargs['rotate'])
            cmds.polyMoveFacet(objectSel, scale=kwargs['scale'])
        else:
            cmds.move(kwargs['translate'][0], 
                    kwargs['translate'][1],
                    kwargs['translate'][2], 
                    objectSel)
            cmds.rotate(kwargs['rotate'][0], 
                    kwargs['rotate'][1],
                    kwargs['rotate'][2], 
                    objectSel)
            cmds.scale(kwargs['scale'][0], 
                    kwargs['scale'][1],
                    kwargs['scale'][2], 
                    objectSel)

    def appliesToLocalComponent(self, objectSel, alias=None, **kwargs):
        '''
            applies the relevant component transformation to 
            selected geometry
        '''
        if alias=='vtx':
            cmds.polyMoveVertex(objectSel, ltx=kwargs['translate'])
            cmds.polyMoveVertex(objectSel, rotate=kwargs['rotate'])
            cmds.polyMoveVertex(objectSel, scale=kwargs['scale'])
        elif alias=='e':
            cmds.polyMoveEdge(objectSel, translate=kwargs['translate'])
            cmds.polyMoveEdge(objectSel, rotate=kwargs['rotate'])
            cmds.polyMoveEdge(objectSel, scale=kwargs['scale'])
        elif alias=='f':
            cmds.polyMoveFacet(objectSel, translate=kwargs['translate'])
            cmds.polyMoveFacet(objectSel, rotate=kwargs['rotate'])
            cmds.polyMoveFacet(objectSel, scale=kwargs['scale'])
        else:
            cmds.move(kwargs['translate'][0], 
                    kwargs['translate'][1],
                    kwargs['translate'][2], 
                    objectSel)
            cmds.rotate(kwargs['rotate'][0], 
                    kwargs['rotate'][1],
                    kwargs['rotate'][2], 
                    objectSel)
            cmds.scale(kwargs['scale'][0], 
                    kwargs['scale'][1],
                    kwargs['scale'][2], 
                    objectSel)

    def applyTransformations(self):
        '''
            evaluates text expressions entered into user interface
        '''
        objectSelected = cmds.ls(selection=True)
        nameList = objectSelected[0].split('.')
        translate = [evaluateExpressions(cmds.textField(self.allEntriesT['translate_' + str(i)], query=True, text=True).strip()) for i in range(3)]
        rotate = [evaluateExpressions(cmds.textField(self.allEntriesR['rotate_' + str(i)], query=True, text=True).strip()) for i in range(3)]
        scaling = [evaluateExpressions(cmds.textField(self.allEntriesS['scale_' + str(i)], query=True, text=True).strip()) for i in range(3)]     
        if self.isGlobal is True:
            try:    
                if nameList[1].startswith('vtx'):
                    self.appliesToGlobalComponent(objectSelected, 'vtx',
                                                translate=translate, 
                                                rotate=rotate, 
                                                scale=scaling)
                elif nameList[1].startswith('f'):
                    self.appliesToGlobalComponent(objectSelected, 'f',
                                                translate=translate, 
                                                rotate=rotate, 
                                                scale=scaling)
                elif nameList[1].startswith('e'): 
                    self.appliesToGlobalComponent(objectSelected, 'e',
                                                translate=translate, 
                                                rotate=rotate, 
                                                scale=scaling)
                elif nameList[1].startswith('vtxFace'):
                    vertNumber = (objectSelected[0].split('[')[1]).split(']')[0]
                    vertex  = nameList[0] + 'vtx[' + vertNumber + ']'
                    self.appliesToGlobalComponent(vertex, 'vtx',
                                                translate=translate, 
                                                rotate=rotate, 
                                                scale=scaling)
                else:
                    self.appliesToGlobalComponent(objectSelected, 
                            translate=translate, 
                            rotate=rotate, 
                            scale=scaling)
            except IndexError:
                self.appliesToGlobalComponent(objectSelected, 'vtx',
                            translate=translate, 
                            rotate=rotate, 
                            scale=scaling)
        elif self.isGlobal is False:
            try:
                if nameList[1].startswith('vtx'):
                    cmds.polyMoveVertex(objectSelected, ltx=translate[0],lty=translate[1],ltz=translate[2])
                    cmds.polyMoveVertex(objectSelected, rx=rotate[0],ry=rotate[1],rz=rotate[2])
                    cmds.polyMoveVertex(objectSelected, sx=scaling[0],sy=scaling[1],sz=scaling[2])
                elif nameList[1].startswith('f'):
                    cmds.polyMoveFacet(objectSelected, ltx=translate[0],lty=translate[1],ltz=translate[2])
                    cmds.polyMoveFacet(objectSelected, lrx=rotate[0],lry=rotate[1],lrz=rotate[2])
                    cmds.polyMoveFacet(objectSelected, lsx=scaling[0],lsy=scaling[1],lsz=scaling[2])
                elif nameList[1].startswith('e'):   
                    cmds.polyMoveEdge(objectSelected, ltx=translate[0],lty=translate[1],ltz=translate[2])
                    cmds.polyMoveEdge(objectSelected, lrx=rotate[0],lry=rotate[1],lrz=rotate[2])
                    cmds.polyMoveEdge(objectSelected, lsx=scaling[0],lsy=scaling[1],lsz=scaling[2])
                elif nameList[1].startswith('vtxFace'):
                    vertNumber = (objectSelected[0].split('[')[1]).split(']')[0]
                    vertex  = nameList[0] + 'vtx[' + vertNumber + ']'
                    cmds.polyMoveVertex(vertex, ltx=translate[0],lty=translate[1],ltz=translate[2])
                    cmds.polyMoveVertex(vertex, rx=rotate[0],ry=rotate[1],rz=rotate[2])
                    cmds.polyMoveVertex(vertex, sx=scaling[0],sy=scaling[1],sz=scaling[2])
                else:
                    cmds.xform(objectSelected, translation=[translate[0], translate[1], translate[2]], relative=True)
                    cmds.xform(objectSelected, rotation=[rotate[0], rotate[1], rotate[2]], euler=True)
                    cmds.xform(objectSelected, scale=[scaling[0], scaling[1], scaling[2]], relative=True)
            except IndexError:
                cmds.xform(objectSelected, translation=[translate[0], translate[1], translate[2]], relative=True)
                cmds.xform(objectSelected, rotation=[rotate[0], rotate[1], rotate[2]], euler=True)
                cmds.xform(objectSelected, scale=[scaling[0], scaling[1], scaling[2]], relative=True)
                
    def chooseWinName(self, *args):
        '''
            if no short window name is supplied, use window long name by default
        '''    
        if type(self.shortName) is None:
            return self.windowName
        else:
            self.windowName = self.shortName
            return self.windowName
    
    @RuntimeErrorDecorator    
    def callBackFunc(self):
        '''
            executes main user interface when geometry is selected
        '''
        cmds.deleteUI(self.mainWindow)
        self.name = self.chooseWinName()
        self.secondWindow = cmds.window(title=self.name, widthHeight = (400, 110), resizeToFitChildren=True, sizeable=False)
        self.deleteCurrentWindow(self.name)  
        cmds.scriptJob(uiDeleted=[self.secondWindow,self.killAllCommands])            
        
        mainLayout = cmds.rowColumnLayout(numberOfColumns=4, columnWidth=[(1,100),(2,100)])
        translation = cmds.text('Translation')
        self.allEntriesT = {'translate_' + str(i): cmds.textField(w=100, text='0') for i in range(3)}
        rotate = cmds.text('Rotation')
        self.allEntriesR = {'rotate_' + str(i): cmds.textField(w=100, text='0') for i in range(3)}
        scale = cmds.text('Scale')
        self.allEntriesS = {'scale_' + str(i): cmds.textField(w=100, text='1') for i in range(3)}
        
        cmds.setParent('..')
        
        cmds.frameLayout('Other Features', w=400)
        cmds.rowColumnLayout(numberOfColumns=3, columnWidth=([1,100],[3,390]))
        cmds.text('Normal Type')
        self.otherEntries['type'] = cmds.checkBox('Global',  onCommand = self.detectType, offCommand = self.detectType)             
        cmds.iconTextButton(image = 'C:\\Users\\Student\\OneDrive - Bournemouth University\\summer_work\\images\\info_icon.png', 
                             command = 'print( UI())' )
        
        cmds.setParent('..')
        buttonLayout = cmds.rowColumnLayout(numberOfColumns=3)
        apply = cmds.button('Apply', command= lambda *args: self.applyTransformations(), w=200)
        undo = cmds.button('Undo', command = self.undoProc, w=200)
        
        cmds.showWindow(self.secondWindow)                  
    
    @RuntimeErrorDecorator    
    def callBackFinished(self):
        '''
            if no geometry is selected, display the secondary window.
        '''
        cmds.deleteUI(self.secondWindow)
        self.name = self.chooseWinName()
        self.mainWindow = cmds.window(title=self.name, widthHeight = (400, 110), resizeToFitChildren=True, sizeable=False)        
        self.deleteCurrentWindow(self.name)
            
        cmds.rowColumnLayout()
        cmds.text('Select an object or polygonal mesh to begin transformations')
        
        cmds.showWindow(self.mainWindow)                        

    
    def killAllCommands(self):
        '''
            kills all jobs related to the program when the application is quit
        '''       
        allJobs = cmds.scriptJob(listJobs=True)
        for i in allJobs:
            jobNumber = int(i.split(':')[0])
            job = i.split(':')[1].strip()
            if job.startswith('ct') or job.startswith('cf'):
                cmds.scriptJob(kill=jobNumber)
        print( 'killed Jobs')
        
        cmds.scriptJob(ct=['SomethingSelected',self.callBackFunc])
        cmds.scriptJob(cf=['SomethingSelected',self.callBackFinished])
        
    def createUI(self):        
        '''
            responsible for displaying the main user interface.
        '''
        
        if isObjectSelected():
            self.name = self.chooseWinName()
            self.mainWindow = cmds.window(title=self.name, widthHeight = (400, 110), resizeToFitChildren=True, sizeable=False)
            self.callBackFunc()
        else:    
            self.name = self.chooseWinName()
            self.mainWindow = cmds.window(title=self.name, widthHeight = (400, 110), resizeToFitChildren=True, sizeable=False)
            self.deleteCurrentWindow(self.name)      
            cmds.rowColumnLayout()
            cmds.text('Select an object or polygonal mesh to begin transformations')     
            
        cmds.scriptJob(ct=['SomethingSelected', self.callBackFunc])                   
        cmds.scriptJob(cf=['SomethingSelected', self.callBackFinished])            
        cmds.scriptJob(uiDeleted=[self.mainWindow,self.killAllCommands])
        
        cmds.showWindow(self.mainWindow)    
        
    def deleteCurrentWindow(self, winID):
        '''
            deletes currently any duplicate windows if they already exist with the specified name
        '''          
        if cmds.window(winID, exists=True):
            cmds.deleteUI(winID)
                                                                        
    def undoProc(self, *args):
        '''
            undo command 
        '''
        cmds.undo()
        
if __name__=='__main__':
    user_interface = UI('Maziar win', 'mWin') 
    print( user_interface )
    user_interface.createUI()