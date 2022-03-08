| mfs scriptFile |
"IMPORTANT: remove or rename the **_control.csv file from the parameters directory, as this file sets a single year"
"for the other control parameters default values will be used"
ModelIO invalidateRootDirectories.
"set the directory with R executables when R should be used to estimate LP50"
RInterface rDirectory: nil. "C:\Progra~1\R\R-3.6.1\bin\x64'."
mfs := (-10 to: 15) collect: [:p | (2 raisedTo: p) asFloat].
scriptFile := LGUTSProject scriptMoSAnalysisGUTSSDMultiplicationFactors: mfs.
"set the years"
years := (1992 to: 2015) asArray.
years do: [:each |
	CatchmentConcDataBase removeAllDataBases.
	CatchmentGUTSSDModelSystem defaultApplicationYear: each.
	(ModelProject fromScriptFile: scriptFile) runModelProjectForeground ].
Smalltalk quitPrimitive
