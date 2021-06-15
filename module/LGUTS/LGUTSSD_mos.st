| mfs scriptFile |
ModelIO invalidateRootDirectories.
CatchmentConcDataBase removeAllDataBases.
RInterface rDirectory: nil. "'C:\Progra~1\R\R-3.5.3\bin\x64'."
mfs := (-10 to: 15) collect: [:p | (2 raisedTo: p) asFloat].
scriptFile := LGUTSProject scriptMoSAnalysisGUTSSDMultiplicationFactors: mfs.
(ModelProject fromScriptFile: scriptFile) runModelProjectForeground.
Smalltalk quitPrimitive
