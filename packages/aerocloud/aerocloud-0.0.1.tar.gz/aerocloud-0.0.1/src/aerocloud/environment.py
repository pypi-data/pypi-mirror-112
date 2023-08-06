import glob
import os

DEFAULT_LOCAL_WORKSPACE = "C:\\temp\\aerocloud"
WORKSPACE_WORKING_DIR = "wd"
WORKSPACE_DATA_DIR = "data"
WORKSPACE_INPUT_DIR = "input"

NODE_ID_ENV_VAR = "AZ_BATCH_NODE_ID"
TASK_DATA_DIR_ENV_VAR = "TASK_DATA_DIR"
TASK_WORKING_DIR_ENV_VAR = "AZ_BATCH_TASK_WORKING_DIR"
TASK_PARENT_TASK_IDS_ENV_VAR = "PARENT_TASK_IDS"


localWorkspace = DEFAULT_LOCAL_WORKSPACE


def isLocal():
    "Gets a value indicating whether the current environment is local (not Azure Batch)."
    return os.environ.get(NODE_ID_ENV_VAR) == None


def getLocalWorkspace():
    "Gets the local workspace path. Returns None if the path doesn't exist."
    return localWorkspace if isLocal() else None


def setLocalWorkspace(path: str = DEFAULT_LOCAL_WORKSPACE, init: bool = True):
    "Sets the local workspace path and (optionally) initialises its internal directory structure."
    if not isLocal():
        return

    global localWorkspace
    localWorkspace = path

    os.makedirs(localWorkspace, exist_ok=True)

    if init:
        os.makedirs(os.path.join(localWorkspace, WORKSPACE_WORKING_DIR), exist_ok=True)
        os.makedirs(os.path.join(localWorkspace, WORKSPACE_DATA_DIR, WORKSPACE_INPUT_DIR), exist_ok=True)


def getWorkingDirectory():
    "Gets the task's working directory. Any resource files uploaded on the activity can be found at this location."
    workingDirectory = os.path.join(localWorkspace, WORKSPACE_WORKING_DIR) if isLocal() else os.environ.get(TASK_WORKING_DIR_ENV_VAR)

    if not os.path.isdir(workingDirectory):
        print(f'Working directory {workingDirectory} does not exist. Did you forget to initialise your local workspace?')

    return workingDirectory


def getDataDirectory():
    "Internal use only."
    return os.path.join(localWorkspace, WORKSPACE_DATA_DIR) if isLocal() else os.environ.get(TASK_DATA_DIR_ENV_VAR)


def getInputDirectory():
    "Gets the activity's input directory. Any output files from the parent activity can be found at this location."
    # Note: The Python activity can only have a single parent.
    parentTaskId = WORKSPACE_INPUT_DIR if isLocal() else os.environ.get(TASK_PARENT_TASK_IDS_ENV_VAR)
    inputDirectory = os.path.join(getDataDirectory(), parentTaskId)

    if not os.path.isdir(inputDirectory):
        print(f'Input directory {inputDirectory} does not exist. Did you forget to initialise your local workspace?')

    return inputDirectory


def getInputFiles(filter: str = "*.*"):
    "Gets the paths of any input files that match the specified glob pattern."
    return glob.glob(os.path.join(getInputDirectory(), filter))


def getResourceFile(name: str):
    "Gets the path of the specified resource file. Returns None if no such file exists."
    path = os.path.join(getWorkingDirectory(), name)
    return path if os.path.exists(path) else None


def getOutputDirectory():
    "Gets the activity's output directory. Any files written to this location will be uploaded as artefacts and available for child activities."
    outputDirectory = getDataDirectory()

    if not os.path.isdir(outputDirectory):
        print(f'Output directory {outputDirectory} does not exist. Did you forget to initialise your local workspace?')

    return outputDirectory
