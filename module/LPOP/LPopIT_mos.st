| mfs scriptFile |
ModelIO invalidateRootDirectories.
"mfs := (-10 to: 15) collect: [:p | (2 raisedTo: p) asFloat]."
mfs := {0.0. 0.1. 1.0. 10.0. 100.0. 1000.0. 10000.0. 100000.0.}.
scriptFile := LPopProject scriptMoSAnalysisLPopITMultiplicationFactors: mfs runs: 1 "2".
(ModelProject fromScriptFile: scriptFile) runModelProjectForeground.
Smalltalk quitPrimitive
