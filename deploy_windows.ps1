# Windows Deployment Script for Employee Onboarding Portal
# Run this script as Administrator

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Please run this script as Administrator" -ForegroundColor Red
    exit
}

# Function to check if a command exists
function Test-Command($Command) {
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

# Check Python installation
if (-not (Test-Command python)) {
    Write-Host "Python is not installed. Please install Python 3.8 or higher from python.org" -ForegroundColor Red
    exit
}

# Check Python version
$pythonVersion = python --version
Write-Host "Python version: $pythonVersion" -ForegroundColor Green

# Create and activate virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    @"
DEBUG=True
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
DATABASE_URL=sqlite:///db.sqlite3
"@ | Out-File -FilePath ".env" -Encoding UTF8
}

# Apply database migrations
Write-Host "Applying database migrations..." -ForegroundColor Yellow
cd onboarding_app
python manage.py migrate

# Create superuser if it doesn't exist
Write-Host "Creating superuser..." -ForegroundColor Yellow
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='e3017847').exists():
    User.objects.create_superuser('e3017847', 'tarun.varshney@example.com', 'Leo@1grip')
"

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Create Windows Service
Write-Host "Creating Windows Service..." -ForegroundColor Yellow
$serviceName = "EmployeeOnboardingPortal"
$serviceExists = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

if (-not $serviceExists) {
    # Create service using NSSM (Non-Sucking Service Manager)
    if (-not (Test-Command nssm)) {
        Write-Host "Installing NSSM..." -ForegroundColor Yellow
        # Download and install NSSM
        $nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
        $nssmZip = "nssm.zip"
        Invoke-WebRequest -Uri $nssmUrl -OutFile $nssmZip
        Expand-Archive -Path $nssmZip -DestinationPath "C:\nssm" -Force
        $env:Path += ";C:\nssm\nssm-2.24\win64"
    }

    # Create the service
    nssm install $serviceName "C:\Python38\python.exe" "C:\path\to\your\project\manage.py runserver 0.0.0.0:8000"
    nssm set $serviceName AppDirectory "C:\path\to\your\project"
    nssm set $serviceName DisplayName "Employee Onboarding Portal"
    nssm set $serviceName Description "Employee Onboarding Portal Service"
    nssm set $serviceName Start SERVICE_AUTO_START
}

# Configure IIS
Write-Host "Configuring IIS..." -ForegroundColor Yellow
# Enable IIS features
Enable-WindowsOptionalFeature -Online -FeatureName "IIS-WebServerRole" -All
Enable-WindowsOptionalFeature -Online -FeatureName "IIS-WebServer" -All
Enable-WindowsOptionalFeature -Online -FeatureName "IIS-CommonHttpFeatures" -All
Enable-WindowsOptionalFeature -Online -FeatureName "IIS-ManagementConsole" -All

# Install URL Rewrite Module
$urlRewriteUrl = "https://download.microsoft.com/download/1/2/8/128E2E22-C1B9-44A4-BE2A-5859ED1D4592/rewrite_amd64_en-US.msi"
$urlRewriteMsi = "rewrite_amd64_en-US.msi"
Invoke-WebRequest -Uri $urlRewriteUrl -OutFile $urlRewriteMsi
Start-Process msiexec.exe -Wait -ArgumentList '/i', $urlRewriteMsi, '/quiet', '/norestart'

# Configure IIS website
Import-Module WebAdministration
$siteName = "EmployeeOnboardingPortal"
$sitePath = "C:\inetpub\wwwroot\EmployeeOnboardingPortal"

if (-not (Test-Path "IIS:\Sites\$siteName")) {
    New-Website -Name $siteName -PhysicalPath $sitePath -Port 80
}

# Set up application pool
$appPoolName = "EmployeeOnboardingPortal"
if (-not (Test-Path "IIS:\AppPools\$appPoolName")) {
    New-WebAppPool -Name $appPoolName
    Set-ItemProperty "IIS:\AppPools\$appPoolName" -name "managedRuntimeVersion" -value ""
    Set-ItemProperty "IIS:\AppPools\$appPoolName" -name "processModel.identityType" -value "ApplicationPoolIdentity"
}

# Configure web.config
$webConfig = @"
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <rewrite>
            <rules>
                <rule name="Django" stopProcessing="true">
                    <match url="(.*)" ignoreCase="false" />
                    <conditions logicalGrouping="MatchAll">
                        <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
                        <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" />
                    </conditions>
                    <action type="Rewrite" url="wsgi.py/{R:1}" />
                </rule>
            </rules>
        </rewrite>
        <handlers>
            <add name="Python FastCGI" path="*" verb="*" modules="FastCgiModule" scriptProcessor="C:\Python38\python.exe|C:\Python38\Lib\site-packages\wfastcgi.py" resourceType="Unspecified" requireAccess="Script" />
        </handlers>
    </system.webServer>
</configuration>
"@

$webConfig | Out-File -FilePath "$sitePath\web.config" -Encoding UTF8

Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "Please review the following:"
Write-Host "1. Update the paths in the Windows Service configuration"
Write-Host "2. Configure your firewall rules"
Write-Host "3. Set up SSL certificate for HTTPS"
Write-Host "4. Change the default superuser password" 