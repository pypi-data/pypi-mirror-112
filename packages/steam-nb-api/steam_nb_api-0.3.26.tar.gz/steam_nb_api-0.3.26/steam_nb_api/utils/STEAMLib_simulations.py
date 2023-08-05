from steam_nb_api.sing.ParametersCOSIM import ParametersCOSIM
from steam_nb_api.utils.misc import makeCopyFile
import datetime
import csv
import os
from pathlib import Path
import numpy as np
import yaml
import shutil
import json
import time
from steam_nb_api.ledet.ParameterSweep import *

def _read_yaml(type_str, elem_name):
    """
    Reads yaml file and returns it as dictionary
    :param type_str: type of file, e.g.: quench, coil, wire
    :param elem_name: file name, e.g. ColSol.1
    :return: dictionary for file named: type.name.yam
    """
    fullfileName = os.path.join(os.getcwd(), f"{type_str}.{elem_name}.yaml")
    with open(fullfileName, 'r') as stream:
        data = yaml.safe_load(stream)
    return data

@dataclass
class Options:
    t_0: np.ndarray = np.array([0,1,2])
    t_end: np.ndarray = np.array([1,2,3])
    t_step_max: np.ndarray = np.array([[0.0005,0.001,0.001]]*2)
    relTolerance: np.ndarray = np.array([1e-4,None])
    absTolerance: np.ndarray = np.array([1,None])
    executionOrder: np.ndarray = np.array([1,2])
    executeCleanRun: np.ndarray = np.array([True, True])

class LibSim_setup:
    def __checkOptions(self):
        for key in self.Options.__annotations__:
            if isinstance(self.Options.__getattribute__(key), list):
                tempv = np.array(self.Options.__getattribute__(key))
                self.Options.__setattr__(key, tempv)
            elif isinstance(self.Options.__getattribute__(key), np.ndarray):
                continue
            else:
                print(key + ' in Options, Data-type not understood. Abort.')

    def __autoConstructOptions(self, N_LEDET):
        if N_LEDET > 1:
            self.Options.t_step_max = np.vstack((self.Options.t_step_max, [self.Options.t_step_max.tolist()[-1]]*(N_LEDET-1)))
            self.Options.relTolerance = np.append(self.Options.relTolerance, [self.Options.relTolerance.tolist()[-1]]*(N_LEDET-1))
            self.Options.absTolerance = np.append(self.Options.absTolerance,
                                                  [self.Options.absTolerance.tolist()[-1]] * (N_LEDET-1))
            self.Options.executionOrder = np.append(self.Options.executionOrder,
                                                  [self.Options.executionOrder.tolist()[-1]] * (N_LEDET-1))
            self.Options.executeCleanRun = np.append(self.Options.executeCleanRun,
                                                    [self.Options.executeCleanRun.tolist()[-1]] * (N_LEDET-1))
        return

    def __init__(self, circuit, ParameterFile, Opts='Default'):
        # Folder and Executables
        self.path_PSPICELib = ''
        self.path_NotebookLib = ''
        self.PspiceExecutable = ''
        self.LedetExecutable = ''
        self.CosimExecutable = ''
        self.Folder = ''
        self.EOS_stub_C = ''
        self.EOS_stub_EOS = ''
        self.PSPICE_Folder = ''

        self.ParameterFile = ParameterFile

        self.circuit = circuit
        self.transient = ''
        self.enableQuench = 0

        if Opts == 'Default':
            self.Options = Options()
            self.flag_Options = 1
        elif Opts == 'Param_Table':
            parameter_dict = self._loadParameterFile()
            self.Options = Options()
            [setattr(self.Options, op_atr, parameter_dict[op_atr]) for op_atr in self.Options.__annotations__]
            self.flag_Options = 0
            self.__checkOptions()
        else:
            self.flag_Options = 0
            self.Options = Opts
            self.__checkOptions()
        self.QuenchMagnet = 0
        self.ManualStimuli = []
        return

    def load_config(self, file=''):
        idx = os.getcwd().index('steam-notebooks')
        self.path_NotebookLib = os.getcwd()[:idx+15]+'//'
        config = os.path.join(self.path_NotebookLib, 'steam-sing-input', 'resources', 'User configurations', 'config')
        if file == '':
            file = os.getenv('JUPYTERHUB_USER')
            if file is None:
                file = os.path.basename(os.path.normpath(os.getenv('Home')))
        config_dict = _read_yaml(config, file)
        self.path_PSPICELib = config_dict['LibraryFolder']
        self.PspiceExecutable = config_dict['PSpiceExecutable']
        self.LedetExecutable = config_dict['LEDETExecutable']
        self.CosimExecutable = config_dict['COSIMExecutable']
        self.Folder = config_dict['Folder']
        self.EOS_stub_C = config_dict['EOS_SynchronizationFolder']

        try:
            EOS_stub_EOS = config_dict['EOS_Base']
        except:
             EOS_stub_EOS = os.environ['SWAN_HOME']
        try:
            self.PSPICE_Folder = config_dict['PSPICE_Folder']
        except:
            self.PSPICE_Folder = ''
        try:
            self.Change_Folder = config_dict['Change_Folder']
        except:
            self.Change_Folder = ''

        self.EOS_stub_EOS = EOS_stub_EOS
        if os.getcwd().startswith('C'):
            self.ModelFolder_EOS = self.Folder
        else:
            self.ModelFolder_EOS = self.Folder.replace(self.EOS_stub_C, EOS_stub_EOS)
            self.ModelFolder_EOS = self.ModelFolder_EOS.replace('\\','//')
        return

    def _loadParameterFile(self):
        with open(self.ParameterFile, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row_parameter = []
            values = []
            parameter_dict = {}

            line_count = 0
            for row in csv_reader:
                if line_count == 0: row_parameter = row
                if row[0] == self.circuit: values = row
                line_count = line_count + 1
            if not values:
                print("Circuit not found in file!")
                return
            for i in range(1,len(row_parameter)):
                try:
                    parameter_dict[row_parameter[i]] = float(values[i])
                except:
                    try:
                        if row_parameter[i] == 'MagnetName' or row_parameter[i] == 'ManualCircuit':
                            parameter_dict[row_parameter[i]] = json.loads(values[i])
                        else:
                            parameter_dict[row_parameter[i]] = json.loads(values[i].lower())
                    except:
                        parameter_dict[row_parameter[i]] = values[i]
        return parameter_dict

    def SetUpSimulation(self, transient, Current='', Append: bool = False, ManualCircuit: str = '', ManualStimuli: list = [],
                        AppendStimuli = '', HierCOSIM = '', convergenceElement = '', CombinedModel = False):
        with open(os.path.join(self.ModelFolder_EOS, 'InSetUp.txt'), 'a') as the_file:
            the_file.write('Temp file to mark running set-up.\n')

        self.transient = transient
        parameter_dict = self._loadParameterFile()

        if ManualStimuli:
            self.ManualStimuli = ManualStimuli
        if 'Quench' in parameter_dict.keys():
            self.enableQuench = parameter_dict['Quench']
        else:
            self.enableQuench = 0

        if Current == 'Param_Table':
            Current = parameter_dict['Current']
        if ManualCircuit == 'Param_Table':
            ManualCircuit = parameter_dict['ManualCircuit']
            ManualCircuit = os.path.join(self.path_NotebookLib, *["steam-sing-input"], *ManualCircuit)
        if convergenceElement == 'Param_Table':
            convergenceElement = parameter_dict['convergenceElement']
        if CombinedModel == 'Param_Table':
            CombinedModel = parameter_dict['CombinedModel']

        if not isinstance(Current, list):
            Current = [Current]

        Folder = []
        for i in range(len(Current)):
            I00 = Current[i]
            parameter_dict['I_00'] = I00
            if 'I00' not in parameter_dict.keys():
                parameter_dict['I00'] = I00
            if ManualStimuli or len(Current)>1 or len(Current[0])>1:
                if not isinstance(parameter_dict['I00'], list):
                    parameter_dict['I00'] = [parameter_dict['I00']]
                if len(parameter_dict['I00'])>1:
                    parameter_dict['I00'] = parameter_dict['I00'][i]

            if parameter_dict['NumberOfMagnets']>1:
                try:
                    MagnetName = parameter_dict['MagnetName']
                    N_LEDET = len(MagnetName)
                except:
                    N_LEDET = 2
                if convergenceElement and not CombinedModel: N_LEDET = 1
            else:
                N_LEDET = 1

            Sim_Flag = parameter_dict['flag_COSIM']
            if Sim_Flag:
                if self.flag_Options and i==0: self.__autoConstructOptions(N_LEDET)
                CoilSections = parameter_dict['CoilSections']
                if not ManualCircuit: circuit_file = self.__findCircuit(self.circuit)
                else: circuit_file = ManualCircuit
                COSIMfolder = self._setUp_COSIM(N_LEDET, CoilSections, circuit_file, parameter_dict, AppendStimuli = AppendStimuli,
                                                HierCOSIM = HierCOSIM, convergenceElement=convergenceElement, CombinedModel = CombinedModel)
            else:
                COSIMfolder = self._setUp_LEDETonly(parameter_dict, HierCOSIM = HierCOSIM)
            Folder.append(COSIMfolder)

        newModelCosim = ParametersCOSIM('1', '1', '1')
        if Sim_Flag:
            newModelCosim.writeCOSIMBatch(Folder, self.CosimExecutable,
                                          Destination=self.ModelFolder_EOS, Append = Append)
        else:
            newModelCosim.writeCOSIMBatch(Folder, self.CosimExecutable,
                                          Destination=self.ModelFolder_EOS, LEDET_exe=self.LedetExecutable, Append = Append)
        time.sleep(30)
        os.remove(os.path.join(self.ModelFolder_EOS, 'InSetUp.txt'))

    def StampBatch(self, Stamp, move_to_mod_fol=False):
        newModelCosim = ParametersCOSIM('1', '1', '1')
        if move_to_mod_fol:
            newModelCosim.StampBatch(Stamp, Folder=f"COSIM_{self.circuit}", Destination=self.ModelFolder_EOS)
        else:
            newModelCosim.StampBatch(Stamp, Folder='', Destination=self.ModelFolder_EOS)

    def __obtainCircuitParameters(self, circuit, new_circuit):
        parameter = {}
        f = open(circuit,'r')
        g = open(new_circuit, 'w')
        flag_On = 0
        for line in f:
            if line.startswith('.PARAM') or line.startswith(' .PARAM') and not '+' in line:
                flag_On = 1
            elif flag_On:
                if line.startswith('+') or line.startswith('*+') or line.startswith('* +'): flag_On = 1
                else: flag_On = 0
            if '+' in line[:10] and not line.startswith('*') and not 'PARAMS' in line and flag_On :
                para = line[line.index('+') + 1:line.index('=')].replace(' ', '')
                parameter[para] = 0
            else:
                g.write(line)
            if '_Quench' in line: self.QuenchMagnet = 1
        return parameter

    def __manipulateCircuit(self, circuit, parameter_dict, Stimuli):
         # 1. Write the params back into .cir
        f = open(circuit, 'r')
        new_lines = []
        flag_unbalancedFPA = 0
        if isinstance(Stimuli, list):
            flag_unbalancedFPA = 1
            StimuliCounter = 0
        for line in f:
            if line.startswith('I_PC') or line.startswith(' I_PC') and not self.ManualStimuli:
                idx = line.index('STIMULUS')
                if flag_unbalancedFPA:
                    ll = line[:idx] + " STIMULUS = " + Stimuli[StimuliCounter] + '\n'
                    StimuliCounter = StimuliCounter +1
                else:
                    ll = line[:idx]+" STIMULUS = "+ Stimuli+'\n'
                line = ll
                new_lines.append(line)
            elif line.startswith('.PARAM') or line.startswith(' .PARAM'):
                new_lines.append(line)
                for key in parameter_dict.keys():
                    if key == 'PowerConverter': continue
                    nl = '+ '+str(key)+'={'+str(parameter_dict[key])+'}\n'
                    new_lines.append(nl)
            elif line.startswith('.LIB') or line.startswith(' .LIB'):
                nel = line.replace("C:\\cernbox\\steam-pspice-library\\", self.path_PSPICELib)
                new_lines.append(nel)
            elif line.startswith('x_PC') or line.startswith(' x_PC'):
                try:
                    PC = parameter_dict['PowerConverter']
                    idx = line.index(')')
                    ll = line[:idx+2] + str(PC) + '\n'
                    line = ll
                    new_lines.append(line)
                except:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        # 2. Include new options
        ## TODO
        g = open(circuit, 'w')
        g.writelines(new_lines)
        return

    def __findCircuit(self, circuitName):
        try:
            idx = circuitName.index('.')
        except:
            idx = circuitName.index('_')
        fam = circuitName[:idx]
        sourcedir = os.listdir(os.path.join(self.path_NotebookLib,'steam-sing-input'))
        for f in sourcedir:
            if os.path.isfile(f): continue
            else:
                files = os.listdir(os.path.join(self.path_NotebookLib,'steam-sing-input',f))
                for k in files:
                    if k.startswith(fam) and k.endswith('Cosim.cir'):
                        return os.path.join(self.path_NotebookLib,'steam-sing-input',f,k)
        print('No circuit file found for' + circuitName + ' [' + fam + '] ')

    def addManualStimuli(self, ManualStimuli):
        self.ManualStimuli = ManualStimuli

    def generateStimuliCOSIM(self, StimulusFile, transient, current_level, t_Start, t_PC, AppendStimuli):
        if transient == 'FPA' and not self.ManualStimuli or transient.startswith(self.circuit):
            current_level = current_level[0]
            Stimuli =  "I_FPA_" + str(current_level)
            stlString = ".STIMULUS I_FPA_" + str(current_level) + " PWL" + "\n"
            stlString = stlString + "+ TIME_SCALE_FACTOR = 1 \n"
            stlString = stlString + "+ VALUE_SCALE_FACTOR = 1 \n"
            stlString = stlString + "+ ( " + str(t_Start)+"s,  " + str(current_level) + "A )\n"
            stlString = stlString + "+ ( " + str(t_PC)+"s,  " + str(current_level) + "A )\n"
            stlString = stlString + "+ ( " + str(t_PC+0.001)+"s,  0A )\n"
            stlString = stlString + "+ ( 70.00000s,  0A )\n"
            stlString = stlString + "\n"
            with open(StimulusFile, 'a') as file:
                file.write(stlString)
        elif transient == 'Constant' and not self.ManualStimuli or transient.startswith(self.circuit):
            current_level = current_level[0]
            Stimuli =  "I_FPA_" + str(current_level)
            stlString = ".STIMULUS I_FPA_" + str(current_level) + " PWL" + "\n"
            stlString = stlString + "+ TIME_SCALE_FACTOR = 1 \n"
            stlString = stlString + "+ VALUE_SCALE_FACTOR = 1 \n"
            stlString = stlString + "+ ( " + str(t_Start)+"s,  " + str(current_level) + "A )\n"
            stlString = stlString + "+ ( " + str(t_PC)+"s,  " + str(current_level) + "A )\n"
            stlString = stlString + "+ ( " + str(t_PC+0.001)+"s,  " + str(current_level) + "A )\n"
            stlString = stlString + "+ ( "+str(t_PC*2) + "s,  " + str(current_level) + "A )\n"
            stlString = stlString + "\n"
            with open(StimulusFile, 'a') as file:
                file.write(stlString)
        elif transient == 'unbalancedFPA' and not self.ManualStimuli:
            Stimuli = []
            stlString = ''
            for i in range(len(current_level)):
                cl = current_level[i]
                Stimuli.append("I_FPA_" +str(cl))
                stlString = stlString + ".STIMULUS I_FPA_" + str(cl) + " PWL" + "\n"
                stlString = stlString + "+ TIME_SCALE_FACTOR = 1 \n"
                stlString = stlString + "+ VALUE_SCALE_FACTOR = 1 \n"
                stlString = stlString + "+ ( " + str(t_Start) + "s,  " + str(cl) + "A )\n"
                stlString = stlString + "+ ( " + str(t_PC) + "s,  " + str(cl) + "A )\n"
                stlString = stlString + "+ ( " + str(t_PC + 0.001) + "s,  0A )\n"
                stlString = stlString + "+ ( 70.00000s,  0A )\n"
                stlString = stlString + "\n"
            with open(StimulusFile, 'a') as file:
                file.write(stlString)
        elif self.ManualStimuli:
            Stimuli = []
            stlString = ''
            for i in range(len(self.ManualStimuli)):
                cl = current_level[i]
                stim = self.ManualStimuli[i]
                Stimuli.append(str(self.ManualStimuli[i]))
                stlString = stlString + ".STIMULUS " + str(self.ManualStimuli[i]) + " PWL" + "\n"
                stlString = stlString + "+ TIME_SCALE_FACTOR = 1 \n"
                stlString = stlString + "+ VALUE_SCALE_FACTOR = 1 \n"
                stlString = stlString + "+ ( " + str(t_Start) + "s,  " + str(cl) + "A )\n"
                stlString = stlString + "+ ( " + str(t_PC) + "s,  " + str(cl) + "A )\n"
                stlString = stlString + "+ ( " + str(t_PC + 0.001) + "s,  0A )\n"
                stlString = stlString + "+ ( 70.00000s,  0A )\n"
                stlString = stlString + "\n"
            with open(StimulusFile, 'a') as file:
                file.write(stlString)
        else:
            print('Transient is not supported yet. Abort!')
            return
        if AppendStimuli:
            stlString = ''
            with open(StimulusFile, 'a') as file:
                with open(AppendStimuli, 'r') as apSt:
                    for line in apSt:
                        if 't_PC+' in line:
                            idx_tPC = line.find('t_PC+')+5
                            count = 0
                            for k in range(len(line)):
                                if line[k+idx_tPC].isdigit() or line[k+idx_tPC] == '.':
                                    count = count + 1
                                elif line[k+idx_tPC] == '*':
                                    break
                            timeAdd = float(line[idx_tPC:idx_tPC+count])
                            line = line.replace('**t_PC+'+str(timeAdd) +'**', str(t_PC+timeAdd))
                        elif '**t_PC**' in line: line = line.replace('**t_PC** ', str(t_PC))
                        stlString = stlString + line
                file.write(stlString)

        return Stimuli

    def _setUp_COSIM(self, N_LEDET, CoilSections, circuit, parameter_dict, AppendStimuli = '', HierCOSIM = '',
                     convergenceElement='', CombinedModel = False):
        current_level = parameter_dict['I_00']
        MagnetName = parameter_dict['MagnetName']

        if isinstance(parameter_dict['MagnetName'],list):
            DistinctMagnets = len(MagnetName)
        else:
            DistinctMagnets = 1

        if self.enableQuench and not HierCOSIM:
            quenchTitle = '_Quench'
        else: quenchTitle = ''

        if isinstance(current_level, list):
            cl = '_'
            for i in range(len(current_level)):
                cl = cl + str(current_level[i])+"A"
        else: cl = "_" +str(current_level)+"A"

        usualTransients = ['FPA','unbalancedFPA']
        if not self.transient in usualTransients: cl = ''

        if not os.path.isdir(os.path.join(self.ModelFolder_EOS, 'COSIM_'+self.circuit+HierCOSIM)):
            os.mkdir(os.path.join(self.ModelFolder_EOS, 'COSIM_'+self.circuit+HierCOSIM))
        if not os.path.isdir(os.path.join(self.ModelFolder_EOS, 'COSIM_'+self.circuit, self.transient + str(cl) +quenchTitle +HierCOSIM)):
            os.mkdir(os.path.join(self.ModelFolder_EOS, 'COSIM_'+self.circuit, self.transient + str(cl) +quenchTitle +HierCOSIM))
        if not os.path.isdir(os.path.join(self.ModelFolder_EOS, 'COSIM_'+self.circuit, self.transient + str(cl) +quenchTitle +HierCOSIM,'Input')):
            os.mkdir(os.path.join(self.ModelFolder_EOS, 'COSIM_'+self.circuit, self.transient + str(cl) +quenchTitle +HierCOSIM,'Input'))
        ModelFolder_EOS = os.path.join(self.ModelFolder_EOS, 'COSIM_'+self.circuit, self.transient + str(cl) +quenchTitle +HierCOSIM,'Input')
        if not self.Change_Folder:
            ModelFolder_C =  self.Folder + '\\COSIM_'+self.circuit +'\\' + self.transient + str(cl) +quenchTitle +HierCOSIM + '\\Input\\'
            ResultFolder_C = self.Folder + '\\COSIM_'+self.circuit +'\\' + self.transient + str(cl) +quenchTitle +HierCOSIM + '\\Output\\'
        else:
            ModelFolder_C = self.Change_Folder + '\\COSIM_' + self.circuit + '\\' + self.transient + str(cl) + quenchTitle + HierCOSIM + '\\Input\\'
            ResultFolder_C = self.Change_Folder + '\\COSIM_' + self.circuit + '\\' + self.transient + str(cl) + quenchTitle + HierCOSIM + '\\Output\\'
        COSIMfolder = ModelFolder_C

        if len(MagnetName)!= N_LEDET: Magnets = [MagnetName] * N_LEDET
        else: Magnets = MagnetName

        newModelCosim = ParametersCOSIM(ModelFolder_EOS, nameMagnet= Magnets , nameCircuit=self.circuit)
        newModelCosim.makeAllFolders(N_LEDET=N_LEDET)

        # 1. Obtain parameter to change
        new_circuit = os.path.join(ModelFolder_EOS, 'PSpice','Circuit.cir')
        parameter_cir = self.__obtainCircuitParameters(circuit, new_circuit)
        # 2. link parameter to parameter list
        cop_parameter_dict = deepcopy(parameter_dict)
        for key in parameter_dict.keys():
            if key not in parameter_cir.keys():
                del cop_parameter_dict[key]
            else:
                parameter_cir[key] = cop_parameter_dict[key]

        try:
            parameter_cir['PowerConverter'] = parameter_dict['PowerConverter']
        except:
            pass

        if isinstance(MagnetName,list):
            if len(MagnetName) == 2:
                if MagnetName[0] == MagnetName[1] and self.QuenchMagnet: DistinctMagnets = 1
            if CombinedModel:
                self.QuenchMagnet = 0
                DistinctMagnets = 1

        # 3. Generate Stimuli file
        StimulusFile =  os.path.join(ModelFolder_EOS, 'PSpice','ExternalStimulus.stl')
        t_Start = parameter_dict['t_Start']
        try:
            t_PC = parameter_dict['t_PC']
            Stimuli = self.generateStimuliCOSIM(StimulusFile, self.transient, current_level, t_Start, t_PC, AppendStimuli)
        except:
            try:
                count = 0
                for k in parameter_dict.keys():
                    if k.startswith('t_PC'):
                        t_PC = parameter_dict[k]
                        if t_PC >= 999: transient = 'Constant'
                        else: transient = self.transient
                        curr_level = current_level[count]
                        if count == 0:
                            Stimuli = [self.generateStimuliCOSIM(StimulusFile, transient, [curr_level], t_Start, t_PC, AppendStimuli)]
                        else:
                            Stimuli.append(self.generateStimuliCOSIM(StimulusFile, transient, [curr_level], t_Start, t_PC, ''))
                        count = count + 1
            except:
                print("No t_PC found. Please add Stimuli manually.")

        # 4. Change .cir file
        self.__manipulateCircuit(new_circuit, parameter_cir, Stimuli)

        # 5. Generate Input/Output etc.
        newModelCosim.copyConfigFiles(N_LEDET=N_LEDET)
        newModelCosim.makeGenericIOPortFiles(CoilSections, ModelFolder_C, ResultFolder_C,
                                             self.PspiceExecutable, self.LedetExecutable, t_0=self.Options.t_0.tolist(), t_end=self.Options.t_end.tolist(),
                                             t_step_max=self.Options.t_step_max.tolist(), relTolerance=self.Options.relTolerance.tolist(),
                                             absTolerance=self.Options.absTolerance.tolist(),
                                             executionOrder=self.Options.executionOrder.tolist(), executeCleanRun=self.Options.executeCleanRun.tolist(),
                                             N_LEDET=N_LEDET, QuenchMagnet=self.QuenchMagnet, DistinctMagnets=DistinctMagnets, convergenceElement = convergenceElement,
                                             CombinedModel = CombinedModel)

        LEDETfiles = newModelCosim.copyCOSIMfiles(new_circuit, StimulusFile, Magnets, N_LEDET=N_LEDET, ManuallyStimulusFile = StimulusFile)
        prepareLEDETFiles = newModelCosim.prepareLEDETFiles(LEDETfiles, N_PAR=N_LEDET)

        idx = 0
        for file in prepareLEDETFiles:
            par_dict = deepcopy(parameter_dict)
            if self.transient == 'unbalancedFPA':
                if len(CoilSections)>1:
                    par_dict['I00'] = parameter_dict['I_00']
                else:
                    del par_dict['I00']
            else:
                del par_dict['I00']

            if 'i_qT' in parameter_dict.keys():
                if isinstance(parameter_dict['i_qT'], list):
                    if isinstance(parameter_dict['i_qT'][idx], list):
                        par_dict['i_qT'] = parameter_dict['i_qT'][idx]
                    elif idx == 0:
                        par_dict['i_qT'] = parameter_dict['i_qT']
                    else:
                        self.enableQuench = 0
                elif idx > 0:
                    self.enableQuench = 0
            if 'tStartQuench' in parameter_dict.keys():
                if isinstance(parameter_dict['tStartQuench'], list):
                    if isinstance(parameter_dict['tStartQuench'][idx], list):
                        par_dict['tStartQuench'] = parameter_dict['tStartQuench'][idx]
                    elif idx == 0:
                        par_dict['tStartQuench'] = parameter_dict['tStartQuench']
                    else:
                        self.enableQuench = 0
                elif idx > 0:
                    self.enableQuench = 0
            self._manipulateLEDETExcel(file, par_dict)
            idx = idx + 1
        currentDT = datetime.datetime.now()
        print('COSIM_model_' + self.circuit + "_" + self.transient + str(cl)+HierCOSIM + " generated.")
        print('Time stamp: ' + str(currentDT))
        print(' ')
        return COSIMfolder

    def __generateStimuliLEDET(self, parameter_dict, HierCOSIM = ''):
        if self.transient == 'FPA' or HierCOSIM:
            current_level = parameter_dict['I00'][0]
            t_PC = parameter_dict['t_PC']
            t_Start = parameter_dict['t_Start']

            I_LUT = [current_level, current_level, 0]
            t_LUT = [t_Start, t_PC, t_PC+0.001]

            parameter_dict["I_PC_LUT"] = I_LUT
            parameter_dict["t_PC_LUT"] = t_LUT
        else:
            print(self.transient+' is not supported yet. Abort!')
        return parameter_dict

    def _setUp_LEDETonly(self, parameter_dict, HierCOSIM = ''):
        current_level = parameter_dict['I_00']
        MagnetName = parameter_dict['MagnetName']

        if HierCOSIM: cl = ''
        else: cl = "_" + str(current_level) + "A"

        if not os.path.isdir(os.path.join(self.ModelFolder_EOS, 'LEDET_model_' + self.circuit+ HierCOSIM )):
            os.mkdir(os.path.join(self.ModelFolder_EOS, 'LEDET_model_' + self.circuit+ HierCOSIM ))
        if not os.path.isdir(os.path.join(self.ModelFolder_EOS, 'LEDET_model_' + self.circuit, self.transient + cl+ HierCOSIM )):
            os.mkdir(os.path.join(self.ModelFolder_EOS, 'LEDET_model_' + self.circuit, self.transient + cl + HierCOSIM ))
        ModelFolder_EOS = os.path.join(self.ModelFolder_EOS, 'LEDET_model_' + self.circuit, self.transient + cl + HierCOSIM)

        if not self.Change_Folder:
            ModelFolder_C = os.path.join(self.Folder + 'LEDET_model_' + self.circuit, self.transient + cl + HierCOSIM)
        else:
            ModelFolder_C = os.path.join(self.Change_Folder + 'LEDET_model_' + self.circuit, self.transient + cl + HierCOSIM)
        COSIMfolder = str(MagnetName) + '_L_' + ModelFolder_C
        newModelCosim = ParametersCOSIM(ModelFolder_EOS, nameMagnet=MagnetName, nameCircuit=self.circuit)
        newModelCosim.makeAllFolders(N_LEDET=1, LEDET_only=1)
        LEDETfiles = newModelCosim.copyCOSIMfiles('0', '0', MagnetName, N_LEDET=1, LEDET_only=1)
        nameFileLEDET = os.path.join(ModelFolder_EOS, "LEDET", "LEDET", MagnetName, "Input", MagnetName + "_0.xlsx")

        parameter_dict = self.__generateStimuliLEDET(parameter_dict, HierCOSIM = HierCOSIM)
        if not "flag_saveMatFile" in parameter_dict.keys():
            parameter_dict["flag_saveMatFile"] = 1
        if not "flag_generateReport" in parameter_dict.keys():
            parameter_dict["flag_generateReport"] = 1
        if not "flag_saveTxtFiles" in parameter_dict.keys():
            parameter_dict["flag_saveTxtFiles"] = 1
        self._manipulateLEDETExcel(nameFileLEDET, parameter_dict, LEDET=1)

        # Display time stamp and end run
        currentDT = datetime.datetime.now()
        print(' ')
        print('LEDET_model_' + self.circuit + "_" + self.transient + cl + HierCOSIM + " generated.")
        print('Time stamp: ' + str(currentDT))
        return COSIMfolder

    def __generateImitate(self, PL, classvalue, value):
        if type(classvalue) == np.ndarray and len(classvalue) > 1 and len(PL.Inputs.nT)==len(classvalue):
            v = deepcopy(classvalue)
            v = np.where(np.logical_or(np.logical_or(np.logical_or(np.equal(PL.Inputs.polarities_inGroup, 0),
                                                                   np.equal(v, 99999)), np.equal(v, 9999)), np.equal(v, 999)), value, v)
        elif type(classvalue) == np.ndarray and len(classvalue) > 1:
            v = deepcopy(classvalue)
            v = np.where(np.logical_or(np.logical_or(np.equal(v, 99999), np.equal(v, 9999)), np.equal(v, 999)), v, value)
        elif type(classvalue) == np.ndarray:
            v = np.array([value])
        elif (type(classvalue) == float or type(classvalue) == int) and type(value) == list:
            v = value[0]
        else:
            v = value
        return v

    def __generateTimeVectorLEDET(self):
        timeSteps = self.Options.t_step_max[-1]
        time_vector = [self.Options.t_0[0], timeSteps[0], self.Options.t_end[0]]
        for i in range(1, len(self.Options.t_0)):
            time_vector = time_vector + [self.Options.t_0[i]+timeSteps[i], timeSteps[i], self.Options.t_end[i]]
        return time_vector

    def _manipulateLEDETExcel(self, file, parameter_dict, LEDET=0):
        PL = ParametersLEDET()
        PL.readLEDETExcel(file, verbose = False)
        time_vector = self.__generateTimeVectorLEDET()
        PL.Options.time_vector_params = time_vector
        PL.Inputs.tQuench = [self.Options.t_0[0]]*len(PL.Inputs.tQuench)

        CurrentsInCoilsections = []
        if 'I00' in parameter_dict.keys() and not LEDET:
            CurrentsInCoilsections = parameter_dict['I00']
            del parameter_dict['I00']

        for key in parameter_dict.keys():
            if key in PL.Inputs.__annotations__:
                if key == 'tStartQuench': continue
                if not isinstance(parameter_dict[key], list):
                    values = self.__generateImitate(PL, PL.getAttribute(getattr(PL, 'Inputs'), key), parameter_dict[key])
                elif len(parameter_dict[key])==1:
                    values = self.__generateImitate(PL, PL.getAttribute(getattr(PL, 'Inputs'), key), parameter_dict[key])
                else: values = parameter_dict[key]
                PL.setAttribute('Inputs', key, values)
            if key in PL.Options.__annotations__:
                PL.setAttribute("Options", key, parameter_dict[key])

        MagName1 = os.path.abspath(os.path.join(os.path.abspath(os.path.join(file, os.pardir)), os.pardir))
        MagName2 = os.path.abspath(os.path.join(MagName1, os.pardir))
        MagName = MagName1.replace(MagName2 + '/', '')
        fieldmaps = os.path.join(self.path_NotebookLib, 'steam-ledet-input', MagName)
        if self.enableQuench:
            calc_tQD = 0
            if 'tStartQuench' not in parameter_dict.keys(): calc_tQD = 1
            elif isinstance(parameter_dict['tStartQuench'],list):
                if isinstance(parameter_dict['tStartQuench'][0], bool): calc_tQD = 1
            if calc_tQD:
                [l, tQD] = PL.adjust_vQ(fieldmaps, Transversaldelay= 'Short')

                if tQD < 0.01:
                    print("Increased detection margin to 10 ms.")
                    tQD = 0.01
                tQD = parameter_dict['t_PC'] - tQD
                tQD = [tQD]*len(parameter_dict['i_qT'])
            else:
                tQD = parameter_dict['tStartQuench']
                if not isinstance(tQD, list): tQD = [tQD]
                tQD = [float(i) for i in tQD]
            if not isinstance(tQD, list): tQD = [tQD]
            i_qT = parameter_dict['i_qT']
            if not isinstance(i_qT, list): i_qT = [i_qT]

            if len(PL.Inputs.iStartQuench) > 1:
                tStartQuench = [9999] * len(PL.Inputs.tStartQuench)
                iStartQuench = np.linspace(1, len(PL.Inputs.vQ_iStartQuench), len(PL.Inputs.vQ_iStartQuench))
                lengthHotSpot_iStartQuench = [0.01] * len(PL.Inputs.vQ_iStartQuench)
                if len(CurrentsInCoilsections)>0:
                    PL.adjust_vQ(fieldmaps, CurrentsInCoilsections=CurrentsInCoilsections)
                vQ_iStartQuench = PL.Inputs.vQ_iStartQuench
            else:
                iStartQuench = []
                tStartQuench = []
                lengthHotSpot_iStartQuench = []
                vQ_iStartQuench = []

            for i in range(len(tQD)):
                t_Q = tQD[i]
                if t_Q<-5: t_Q = -5
                if len(PL.Inputs.iStartQuench)>1:
                    tStartQuench[int(i_qT[i]) - 1] = t_Q
                    lengthHotSpot_iStartQuench = [0.01] * len(PL.Inputs.vQ_iStartQuench)
                    vQ_iStartQuench[int(i_qT[i]) - 1]= vQ_iStartQuench[int(i_qT[i])  - 1] * 2
                else:
                    iStartQuench.append(int(i_qT[i]))
                    tStartQuench.append(t_Q)
                    lengthHotSpot_iStartQuench.append(0.01)
                    vQ_iStartQuench.append(PL.Inputs.vQ_iStartQuench[int(i_qT[i]) -1]*2)

            PL.setAttribute("Inputs", "iStartQuench", iStartQuench)
            PL.setAttribute("Inputs", "lengthHotSpot_iStartQuench", lengthHotSpot_iStartQuench)
            PL.setAttribute("Inputs", "vQ_iStartQuench", vQ_iStartQuench)
            PL.Inputs.tQuench = [min(tQD)] * len(PL.Inputs.tQuench)
        else:
            tStartQuench = [9999] * len(PL.Inputs.tStartQuench)
            if len(CurrentsInCoilsections) > 0:
                PL.adjust_vQ(fieldmaps, CurrentsInCoilsections=CurrentsInCoilsections)
                PL.setAttribute("Inputs", "iStartQuench", np.linspace(1,len(PL.Inputs.vQ_iStartQuench),len(PL.Inputs.vQ_iStartQuench)))
                PL.setAttribute("Inputs", "lengthHotSpot_iStartQuench", [0.01]*len(PL.Inputs.vQ_iStartQuench))
                tStartQuench = [9999] * len(PL.Inputs.vQ_iStartQuench)

                HalfTurnToGroup = np.repeat(PL.Inputs.GroupToCoilSection, PL.Inputs.nT.astype(int))
                lastj = 0
                for j in PL.Inputs.el_order_half_turns:
                    if HalfTurnToGroup[int(j-1)] != HalfTurnToGroup[lastj-1] and lastj != 0:
                        PL.Inputs.vQ_iStartQuench[int(j-1)] = 0
                        PL.Inputs.lengthHotSpot_iStartQuench[int(j-1)] = 0
                    lastj = int(j)

        PL.setAttribute("Inputs", "tStartQuench", tStartQuench)

        if '#HeatingStations' in parameter_dict.keys():
            [_, th_con_h, th_con_w] = PL._obtainThermalConnections()
            PL.adjust_vQ_QuenchHeater(th_con_h, th_con_w, parameter_dict['#HeatingStations'])

        if 'U_inductive_dynamic_CoilSections' not in PL.Variables.variableToSaveTxt:
            PL.Variables.variableToSaveTxt = np.append(PL.Variables.variableToSaveTxt, 'U_inductive_dynamic_CoilSections')
            PL.Variables.typeVariableToSaveTxt = np.append(PL.Variables.typeVariableToSaveTxt, 1)

        PL.writeFileLEDET(file, verbose = False)
