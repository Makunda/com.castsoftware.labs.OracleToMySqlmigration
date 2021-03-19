@echo off
MODE CON: COLS=132 LINES=40

::Parameters to adapt to each analysis env :
Set SourceFolder=C:\Oxygenworkspacedb2oraclemigration\com.castsoftware.labs.db2oraclemigration\DevTools
Set TargetFolder=C:\Oxygenworkspacedb2oraclemigration\com.castsoftware.labs.db2oraclemigration\MasterFiles
Set adgMetrics=AdgMetrics_db2oraclemigration.xml

::Parameters to adapt in some cases :
Set MetricsCompiler_BAT_path=.\MetricsCompiler.bat


Title Generating %adgMetrics% from MASTER FILES at %TargetFolder%

:: call Compiler - full syntax (with specific AdgConfigData file name)
call %MetricsCompiler_BAT_path% -encodeUA -inputdir %TargetFolder% -outputdir %SourceFolder% -filename %adgMetrics%

::TOBE : Manage ERRORLEVEL ?
pause