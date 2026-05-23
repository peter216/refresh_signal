Set oShell  = CreateObject("WScript.Shell")
Set fso     = CreateObject("Scripting.FileSystemObject")

scriptDir  = fso.GetParentFolderName(WScript.ScriptFullName)
logFile    = scriptDir & "\run_hidden.log"

Sub VbsLog(msg)
    Dim f
    Set f = fso.OpenTextFile(logFile, 8, True)  ' 8 = append, create if missing
    f.WriteLine Now & "  " & msg
    f.Close
End Sub

VbsLog "START ScriptDir=" & scriptDir

' Allow overriding Python executable via PYTHON_EXE env var.
' ExpandEnvironmentStrings returns the literal "%PYTHON_EXE%" when unset, so
' compare against the unexpanded form rather than an empty string.
pythonExe = oShell.ExpandEnvironmentStrings("%PYTHON_EXE%")
If pythonExe = "%PYTHON_EXE%" Or pythonExe = "" Then
    pythonExe = "python"
End If
VbsLog "pythonExe=" & pythonExe

' Build script path from the same directory this VBScript lives in so it
' works regardless of USERPROFILE or working directory set by Task Scheduler.
scriptPath = scriptDir & "\refresh_signal.py"
VbsLog "scriptPath=" & scriptPath

If Not fso.FileExists(scriptPath) Then
    VbsLog "ERROR: refresh_signal.py not found at " & scriptPath
    WScript.Quit 1
End If

cmd = """" & pythonExe & """ """ & scriptPath & """"
VbsLog "Running: " & cmd

oShell.Run cmd, 0, False
VbsLog "END (process launched)"
