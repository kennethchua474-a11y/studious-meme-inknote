; installer.iss

[Setup]
AppName=InkNote
AppVersion=0.2.6
DefaultDirName={pf}\InkNote
DefaultGroupName=InkNote
OutputBaseFilename=InkNote-Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\InkNote\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\InkNote"; Filename: "{app}\InkNote.exe"
Name: "{commondesktop}\InkNote"; Filename: "{app}\InkNote.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\InkNote.exe"; Description: "Launch InkNote"; Flags: nowait postinstall skipifsilent
