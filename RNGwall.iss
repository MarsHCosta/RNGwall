#define MyAppName "RNGwall"
#define MyAppVersion "1.0"

; Uncomment the appropriate line based on your Python/application architecture
#define MyAppArchitecture "x64"
;#define MyAppArchitecture "x86"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
WizardStyle=modern
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppName}.exe
Compression=lzma2
SolidCompression=yes
OutputDir=installer_output
OutputBaseFilename={#MyAppName}_setup_{#MyAppVersion}_{#MyAppArchitecture}
SetupIconFile=icons\RNGwall.ico

; Uncomment the appropriate lines based on your Python/application architecture
;ArchitecturesAllowed=x64
;ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\{#MyAppName}.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "icons\RNGwall.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppName}.exe"; IconFilename: "{app}\RNGwall.ico"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppName}.exe"; IconFilename: "{app}\RNGwall.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked