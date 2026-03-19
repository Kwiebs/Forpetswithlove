# OpenClaw Heartbeat Configuration

# Smart monitoring that runs 3x daily without interrupting production systems
# Leverages existing weather bot while adding proactive intelligence

## Daily Health & Maintenance Cycle

### 🌅 Morning Briefing (09:00 WET)
- **Task Completion Check**: Read ~/workspace/TASKS.md and report status
- **Sub-agent Follow-up**: Check tasks marked "in-progress" >2 hours, ping André if stuck
- **Weather Bot Health Check**: Verify tide data source connectivity
- **System Resource Status**: Memory, disk, load average review  
- **Memory Maintenance**: Clean daily logs older than 7 days
- **Quick Maritime Summary**: Today's fishing conditions (if significant change)

### 🌆 Evening Summary (18:00 WET)
- **Task Status Report**: Update André on active tasks from TASKS.md
- **Sub-agent Status**: List pending sub-agent sessions and their last activity
- **Daily System Report**: Resource trends, service status
- **Weather Bot Performance**: Uptime, data fresheness check
- **Tomorrow's Outlook**: Next day fishing/maritime conditions
- **Maintenance Reminders**: Disk usage alerts, backup suggestions

### 🌙 Overnight Check (02:00 WET)  
- **Task Clean-up**: Archive completed tasks >7 days old to bottom of TASKS.md
- **Deep System Health**: Comprehensive service scan
- **Weekly Memory Cleanup**: Archive significant events to MEMORY.md
- **Performance Trends**: Load, memory, disk growth analysis
- **Critical Alerts Only**: Major issues or service failures

## Alert Rules (Only Important Stuff)

🟢 **ALWAYS QUIET** (23:00-08:00 WET):
- No notifications during sleep hours
- Log significant events for morning review

🟡 **MORNING BRIEFINGS** (09:00 UTC only):
- Weather bot offline >30 minutes
- System resources >80% usage  
- Daily memory cleanup needed
- Significant maritime condition changes
- **Task stuck in "in-progress" >2 hours** — ask André for status
- **Sub-agent not responding** — report session details

🔴 **IMMEDIATE ALERTSANYTIME**:
- Weather bot completely down >1 hour
- System load >5.0 or Memory >90%
- Disk usage >90% or <5GB free
- Failed OpenClaw services detected

## Integration Points

### Weather Bot Monitoring
- Check bot script process status
- Verify Portuguese data source connectivity  
- Monitor telegram webhook responses
- Track forecast generation timestamps

### Smart Notifications
- "Weather: Excellent conditions today - perfect fishing weather!"
- "System: Memory usage up 5% - normal growth pattern"
- "Maintenance: Weekly cleanup completed - 15 files archived"
- "Alert: Weather bot disconnected - investigating..."
- "Tasks update: 2 active tasks, 1 stuck in-progress >2h"

## Operational Safety

✅ **Non-Intrusive**: Never restarts or modifies running services
✅ **Read-Only Checks**: Monitor, don't interfere with production  
✅ **Graceful Degradation**: Skip tasks if systems are under heavy load
✅ **Minimal Overhead**: Check every 8 hours, not constantly

---

*This configuration provides proactive intelligence while respecting production systems*
