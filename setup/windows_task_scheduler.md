# Windows Task Scheduler Setup

Run the Watchdog (which manages the Orchestrator) as a background service that
starts on boot and restarts on failure.

## Step 1 — Create the Task

Open PowerShell as Administrator and run:

```powershell
$action = New-ScheduledTaskAction `
    -Execute "python" `
    -Argument "E:\AI-exam-tutor\watchdog.py" `
    -WorkingDirectory "E:\AI-exam-tutor"

$trigger = New-ScheduledTaskTrigger -AtStartup

$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0) `
    -RestartCount 10 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -RunOnlyIfNetworkAvailable $true

Register-ScheduledTask `
    -TaskName "ExamTutor-Watchdog" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -RunLevel Highest `
    -Description "AI Exam Tutor Watchdog Process Manager"
```

## Step 2 — Start it now (without reboot)

```powershell
Start-ScheduledTask -TaskName "ExamTutor-Watchdog"
```

## Step 3 — Verify it's running

```powershell
Get-ScheduledTask -TaskName "ExamTutor-Watchdog" | Select-Object State
```

## Step 4 — Check logs

```
E:\AI-exam-tutor\logs\orchestrator.stdout.log
E:\AI-exam-tutor\logs\orchestrator.stderr.log
E:\AI-exam-tutor\logs\pipeline\YYYY-MM-DD.json
```

## To stop

```powershell
Stop-ScheduledTask -TaskName "ExamTutor-Watchdog"
Unregister-ScheduledTask -TaskName "ExamTutor-Watchdog" -Confirm:$false
```

## Alternative: PM2 (cross-platform)

```bash
npm install -g pm2
pm2 start watchdog.py --interpreter python3 --name exam-tutor-watchdog
pm2 save
pm2 startup
```
