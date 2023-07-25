import os
import shutil
import json
import argparse


# GLOBAL VARIABLES
programName = "proBuild"
programDesc = "Easy build system that uses Python and Cmake"

projectFile = "." + programName + ".prj"
projectFilesCleanable = ["Makefile", "CMakeCache.txt", "cmake_install.cmake"]
projectDirsCleanable = ["build", "CMakeFiles"]
projectCMakeFile = "cmakelists.txt"
projectBuildCommand = "cmake . -G \"Unix Makefiles\" && make"

#ARGUMENTS
argParser = argparse.ArgumentParser(prog=programName, description=programDesc, epilog="")

argParser.add_argument("mode", choices=["genProjectFile", "build", "clean", "run", "test", "genCmake", "genProjectFileExample"], type=str, help="generate project file, build, cleanup files, run, test (build and run), generate cmakelists.txt, generate an example")
args = argParser.parse_args()

def generateCmakeListsFile(build = False, cleanup = False, run = False):
    f = open(projectFile, "r")
    projectFileContents = f.read()
    projectFileContents = json.loads(projectFileContents)
    f.close()
    
    if(build == False and cleanup == False and run == True):
        for project in projectFileContents["projects"]:
            runCommand  = project["runCommand"]
            os.system(runCommand)
        return


    for project in projectFileContents["projects"]:
        #cmake variables
        cmakeFile = ""
        
        cmake_projectName = str(project["projectName"])
        cmake_cxx_standard = str(project["cxxStandard"])
        cmake_c_compiler = str(project["cCompiler"])
        cmake_cxx_compiler = str(project["cxxCompiler"])
        cmake_sourceDirs  = project["sourceDirs"]
        cmake_includeDirs  = project["includeDirs"]
        cmake_includeDirsPublic  = project["includeDirsPublic"]
        cmake_libraryDirs  = project["libraryDirs"]
        cmake_libraries  = project["libraries"]
        cmake_librariesPublic  = project["librariesPublic"]
        outDir  = project["outDir"]
        runCommand  = project["runCommand"]
        
        #write to string
        cmakeFile += "cmake_minimum_required(VERSION 3.10)\nset(CMAKE_CXX_STANDARD " + cmake_cxx_standard + ")\n"
        cmakeFile += "set(CMAKE_CXX_STANDARD_REQUIRED ON)\n"
        cmakeFile += "set(CMAKE_CXX_FLAGS \"${CMAKE_CXX_FLAGS} -static-libgcc -static-libstdc++\")\n"
        cmakeFile += "set(CMAKE_C_COMPILER " + cmake_c_compiler + ")\n"
        cmakeFile += "set(CMAKE_CXX_COMPILER " + cmake_cxx_compiler + ")\n"
        cmakeFile += "set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/" + outDir + ")\n"
        cmakeFile += "set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/" + outDir + ")\n"
        cmakeFile += "set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/" + outDir + ")\n"
        cmakeFile += "project(" + cmake_projectName + " VERSION 1.0)\n"
        
        srcFiles = ""
        for srcDir in cmake_sourceDirs:
            srcFiles += " " + srcDir + "/*.cpp"
        
        cmakeFile += "file(GLOB_RECURSE SRC_FILES" + srcFiles +")\n" # todo all sources
        cmakeFile += "add_executable(" + cmake_projectName + " ${SRC_FILES})\n"
        
        # PRIVATE INCLUDES
        inclFiles = ""
        for inclDir in cmake_includeDirs:
            inclFiles +=  " " + inclDir
        
        cmakeFile += "target_include_directories(" + cmake_projectName + " PRIVATE "+ inclFiles +")\n"
        
        # PUBLIC INCLUDES
        inclFiles = ""
        for inclDir in cmake_includeDirsPublic:
            inclFiles +=  " " + inclDir
        
        cmakeFile += "target_include_directories(" + cmake_projectName + " PUBLIC "+ inclFiles +")\n"
        
        libDirs = ""
        for libDir in cmake_libraryDirs:
            libDirs += " " + libDir
        
        # PRIVATE LIBRARIES
        for lib in cmake_libraries:
            cmakeFile += "find_library(" + cmake_projectName + lib + "LIB_VAR " + lib + " PATHS " + libDirs + ")\n"
        for lib in cmake_libraries:
            cmakeFile += "target_link_libraries(" + cmake_projectName + " PRIVATE ${" + cmake_projectName + lib + "LIB_VAR})\n"
        
        # PUBLIC LIBRARIES
        for lib in cmake_librariesPublic:
            cmakeFile += "find_library(" + cmake_projectName + lib + "LIB_VAR_PUBLIC " + lib + " PATHS " + libDirs + ")\n"
        for lib in cmake_librariesPublic:
            cmakeFile += "target_link_libraries(" + cmake_projectName + " PUBLIC ${" + cmake_projectName + lib + "LIB_VAR_PUBLIC})\n"
        
        # PUBLIC MISSING
        
        #write string to file
        f = open(projectCMakeFile, "w")
        f.write(cmakeFile)
        f.close()
        
        if(build == True):
            os.system(projectBuildCommand)
        
        if(cleanup == True):
            for cleanable in projectFilesCleanable:
                if(os.path.exists(cleanable)):
                    os.remove(cleanable)
            if(os.path.exists(projectDirsCleanable[1])):
                    shutil.rmtree(projectDirsCleanable[1], ignore_errors=True)
            if(os.path.exists(projectCMakeFile)):
                os.remove(projectCMakeFile)
        
        if(run == True):
            os.system(runCommand)

#CHECK FOR PROJECT FILE
if(not os.path.exists(projectFile) or args.mode == "genProjectFile"):
    emptyConfig = {
    "projects" : [ 
    {"projectName" : "untitled", "cxxStandard" : 17, "cCompiler" : "gcc", "cxxCompiler" : "g++", "sourceDirs" : ["src"], 
    "includeDirs" : ["include"], "includeDirsPublic" : [], "libraryDirs" : [], 
    "libraries" : [], "librariesPublic" : [], "outDir" : "build/bin", "runCommand" : "build\\bin\\untitled.exe"}
    ] }
    
    f = open(projectFile, "w+")
    f.write(json.dumps(emptyConfig))
    f.close()
    
if(args.mode == "genProjectFileExample"):
    exampleConfig = {
            "projects" : [ 
            {"projectName" : "GLFW_Window", "cxxStandard" : 17, "cCompiler" : "gcc", "cxxCompiler" : "g++", "sourceDirs" : ["src", "src2"], 
            "includeDirs" : ["include", "D:/dev/libs/glfw/include"], "includeDirsPublic" : [], "libraryDirs" : ["D:/dev/libs/glfw/lib-mingw-w64"], 
            "libraries" : ["glfw3"], "librariesPublic" : [], "outDir" : "build/bin", "runCommand" : "build\\bin\\GLFW_Window.exe"}
        ] }
    f = open(projectFile, "w+")
    f.write(json.dumps(exampleConfig))
    f.close()


#MODE CLEAN
if(args.mode == "clean"):
    for cleanable in projectFilesCleanable:
        if(os.path.exists(cleanable)):
            os.remove(cleanable)
    for cleanable in projectDirsCleanable:
        if(os.path.exists(cleanable)):
            shutil.rmtree(cleanable, ignore_errors=True)
    
    
    if(os.path.exists(projectCMakeFile)):
        os.remove(projectCMakeFile)

#MODE BUILD
if(args.mode == "build"):
    if(not os.path.exists(projectCMakeFile)):
        f = open(projectCMakeFile, "w+")
        f.close()
    
    generateCmakeListsFile(build=True, cleanup=True)
    
#MODE RUN
if(args.mode == "run"):
    generateCmakeListsFile(build = False, cleanup = False, run = True)

#MODE RUN / TEST
if(args.mode == "test"):
    generateCmakeListsFile(build = True, cleanup = True, run = True)

#MODE GEN CMAKE
if(args.mode == "genCmake"):
    generateCmakeListsFile(build=False, cleanup=False, run=False)
