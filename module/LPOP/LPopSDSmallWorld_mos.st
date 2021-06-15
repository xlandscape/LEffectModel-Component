| mfs scriptFile |
ModelIO invalidateRootDirectories.
mfs := (-10 to: 15) collect: [:p | (2 raisedTo: p) asFloat].
scriptFile := LPopProject scriptMoSAnalysisLPopSDSmallMultiplicationFactors: mfs runs: 5.
(ModelProject fromScriptFile: scriptFile) runModelProjectForeground.
Smalltalk quitPrimitive
	