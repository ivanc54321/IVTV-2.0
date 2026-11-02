Set oShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
desktopPath = oShell.SpecialFolders("Desktop")
startMenuPath = oShell.SpecialFolders("Programs")
iconPath = scriptDir & "\assets\ivtv.ico"
winDir = oShell.ExpandEnvironmentStrings("%SystemRoot%")
wscriptExe = winDir & "\System32\wscript.exe"

' 1. Delete all old standalone shortcuts and legacy variations from Desktop & Start Menu
Dim oldShortcuts, scName
oldShortcuts = Array( _
    desktopPath & "\IV - TV (App Mode).lnk", _
    desktopPath & "\IVTV.lnk", _
    desktopPath & "\IV - TV.lnk", _
    desktopPath & "\IV-TV.lnk", _
    desktopPath & "\IVTV - Live TV.lnk", _
    desktopPath & "\Stop IV - TV.lnk", _
    desktopPath & "\Launch IV - TV.bat", _
    desktopPath & "\IV - TV (Standalone).bat", _
    startMenuPath & "\IV - TV.lnk", _
    startMenuPath & "\IVTV.lnk", _
    startMenuPath & "\Stop IV - TV.lnk" _
)

For Each scName In oldShortcuts
    If fso.FileExists(scName) Then
        On Error Resume Next
        fso.DeleteFile scName, True
        On Error GoTo 0
    End If
Next

' 2. Create the brand new primary Standalone App shortcut on Desktop: "IV - TV.lnk" and "IV - TV 2.0.lnk"
Set scMain = oShell.CreateShortcut(desktopPath & "\IV - TV.lnk")
scMain.TargetPath = wscriptExe
scMain.Arguments = """" & scriptDir & "\launch.vbs"""
scMain.WorkingDirectory = scriptDir
If fso.FileExists(iconPath) Then
    scMain.IconLocation = iconPath & ", 0"
End If
scMain.Description = "IVTV 2.0 - Cinematic UK Freeview & Sky TV Player (Standalone Desktop App)"
scMain.Save

Set scMain2 = oShell.CreateShortcut(desktopPath & "\IV - TV 2.0.lnk")
scMain2.TargetPath = wscriptExe
scMain2.Arguments = """" & scriptDir & "\launch.vbs"""
scMain2.WorkingDirectory = scriptDir
If fso.FileExists(iconPath) Then
    scMain2.IconLocation = iconPath & ", 0"
End If
scMain2.Description = "IVTV 2.0 - Cinematic UK Freeview & Sky TV Player (Standalone Desktop App)"
scMain2.Save

Set scMain3 = oShell.CreateShortcut(desktopPath & "\IVTV 2.0.lnk")
scMain3.TargetPath = wscriptExe
scMain3.Arguments = """" & scriptDir & "\launch.vbs"""
scMain3.WorkingDirectory = scriptDir
If fso.FileExists(iconPath) Then
    scMain3.IconLocation = iconPath & ", 0"
End If
scMain3.Description = "IVTV 2.0 - Cinematic UK Freeview & Sky TV Player (Standalone Desktop App)"
scMain3.Save

' 3. Create the direct Standalone Batch Launcher on Desktop: "IV - TV (Standalone).bat"
Dim batContent, batPath
batPath = desktopPath & "\IV - TV (Standalone).bat"
batContent = "@echo off" & vbCrLf & _
             "cd /d """ & scriptDir & """" & vbCrLf & _
             "start """" """ & wscriptExe & """ """ & scriptDir & "\launch.vbs""" & vbCrLf & _
             "exit /b 0" & vbCrLf

On Error Resume Next
Dim batFile
Set batFile = fso.CreateTextFile(batPath, True)
batFile.Write batContent
batFile.Close
Set batFile = Nothing
On Error GoTo 0

' 4. Create the Stop Server shortcut on Desktop: "Stop IV - TV.lnk"
Set scStop = oShell.CreateShortcut(desktopPath & "\Stop IV - TV.lnk")
scStop.TargetPath = wscriptExe
scStop.Arguments = """" & scriptDir & "\stop.vbs"""
scStop.WorkingDirectory = scriptDir
scStop.IconLocation = "shell32.dll, 27" ' Red power stop icon
scStop.Description = "Stop IV TV Background Server"
scStop.Save

' 5. Register in Windows Start Menu Programs
If fso.FolderExists(startMenuPath) Then
    Set scStart = oShell.CreateShortcut(startMenuPath & "\IV - TV 2.0.lnk")
    scStart.TargetPath = wscriptExe
    scStart.Arguments = """" & scriptDir & "\launch.vbs"""
    scStart.WorkingDirectory = scriptDir
    If fso.FileExists(iconPath) Then
        scStart.IconLocation = iconPath & ", 0"
    End If
    scStart.Description = "IVTV 2.0 - Cinematic UK Freeview & Sky TV Player"
    scStart.Save

    Set scStart2 = oShell.CreateShortcut(startMenuPath & "\IV - TV.lnk")
    scStart2.TargetPath = wscriptExe
    scStart2.Arguments = """" & scriptDir & "\launch.vbs"""
    scStart2.WorkingDirectory = scriptDir
    If fso.FileExists(iconPath) Then
        scStart2.IconLocation = iconPath & ", 0"
    End If
    scStart2.Description = "IVTV 2.0 - Cinematic UK Freeview & Sky TV Player"
    scStart2.Save
End If

WScript.Echo "========================================================"
WScript.Echo "  IVTV 2.0 Standalone Desktop App Updated & Created!"
WScript.Echo "========================================================"
WScript.Echo "Desktop App Shortcut:      " & desktopPath & "\IV - TV 2.0.lnk"
WScript.Echo "Desktop App Shortcut:      " & desktopPath & "\IV - TV.lnk"
WScript.Echo "Desktop Direct Launcher:   " & desktopPath & "\IV - TV (Standalone).bat"
WScript.Echo "Stop Server Shortcut:      " & desktopPath & "\Stop IV - TV.lnk"
If fso.FolderExists(startMenuPath) Then
    WScript.Echo "Start Menu Shortcut:       " & startMenuPath & "\IV - TV 2.0.lnk"
    WScript.Echo "Start Menu Shortcut:       " & startMenuPath & "\IV - TV.lnk"
End If
WScript.Echo "========================================================"

