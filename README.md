# proBuild
Compiling C/C++ code yourself is too hard/annoying? Make is impossible to understand and even Cmake has a terrible syntax? Use proBuild! It's a simple python script which generates CmakeLists.txt files for your project!

## Get it
copy the script
or
```
git clone https://github.com/LED-reamer/proBuild.git
```

## Usage
```
proBuild.py [-h]
            {genProjectFile,build,clean,run,test,genCmake,genProjectFileExample}
```

## Example
```
proBuild.py genProjectFile
```
Creates a ".proBuild.prj" file where you can modify the configurations for your project
```
{
	"projects": [
		{
			"projectName": "untitled",
			"cxxStandard": 17,
			"cCompiler": "gcc",
			"cxxCompiler": "g++",
			"sourceDirs": [
				"src"
			],
			"includeDirs": [
				"include"
			],
			"includeDirsPublic": [],
			"libraryDirs": [],
			"libraries": [],
			"librariesPublic": [],
			"outDir": "build/bin",
			"runCommand": "build\\bin\\untitled.exe"
		}
	]
}
```
Then build and run your project:
```
proBuild.py build
proBuild.py run
```
or
```
proBuild.py test
```
