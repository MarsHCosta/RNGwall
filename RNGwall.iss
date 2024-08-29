[Setup]
AppName=RNGwall
AppVersion=1.0
WizardStyle=modern
DefaultDirName={autopf}\RNGwall
DefaultGroupName=RNGwall
UninstallDisplayIcon={app}\RNGwall.exe
Compression=lzma2
SolidCompression=yes
OutputDir=userdocs:Inno Setup Examples Output

[Files]
Source: "dist\RNGwall.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\RNGwall"; Filename: "{app}\RNGwall.exe"
Name: "{commondesktop}\RNGwall"; Filename: "{app}\RNGwall.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked