[Setup]
AppName=TeacherDesk Pro
AppVersion=1.0
AppPublisher=TeacherDesk
DefaultDirName={autopf}\TeacherDesk Pro
DefaultGroupName=TeacherDesk Pro
OutputDir=installer
OutputBaseFilename=TeacherDeskPro_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source="dist\TeacherDeskPro.exe"; DestDir="{app}"; Flags: ignoreversion
Source="dist\data"; DestDir="{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\TeacherDesk Pro"; Filename: "{app}\TeacherDeskPro.exe"
Name: "{commondesktop}\TeacherDesk Pro"; Filename: "{app}\TeacherDeskPro.exe"

[Run]
Filename: "{app}\TeacherDeskPro.exe"; Description: "Ejecutar TeacherDesk Pro"