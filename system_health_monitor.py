"""
system_health_monitor.py
------------------------
Monitors CPU, Memory, and Disk usage of the system.
Prints a health report and alerts if any metric crosses a threshold.

Author : Sohan R Baadkar
Purpose: TechOps automation — routine system health check script
"""

import psutil
import datetime

# ── Thresholds (in %) ─────────────────────────────────────────────────────────
CPU_THRESHOLD    = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD   = 85


def get_cpu_usage():
    """Returns current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    """Returns used memory percentage and used/total in GB."""
    mem = psutil.virtual_memory()
    used_gb  = mem.used  / (1024 ** 3)
    total_gb = mem.total / (1024 ** 3)
    return mem.percent, used_gb, total_gb


def get_disk_usage(path="/"):
    """Returns disk usage percentage and used/total in GB for given path."""
    disk = psutil.disk_usage(path)
    used_gb  = disk.used  / (1024 ** 3)
    total_gb = disk.total / (1024 ** 3)
    return disk.percent, used_gb, total_gb


def check_status(value, threshold):
    """Returns ALERT if value exceeds threshold, else OK."""
    return "⚠  ALERT" if value >= threshold else "✓  OK"


def print_report():
    """Prints a full system health report to the console."""

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cpu_pct                          = get_cpu_usage()
    mem_pct, mem_used, mem_total     = get_memory_usage()
    disk_pct, disk_used, disk_total  = get_disk_usage()

    cpu_status  = check_status(cpu_pct,  CPU_THRESHOLD)
    mem_status  = check_status(mem_pct,  MEMORY_THRESHOLD)
    disk_status = check_status(disk_pct, DISK_THRESHOLD)

    print("=" * 50)
    print("       SYSTEM HEALTH MONITOR REPORT")
    print(f"       {now}")
    print("=" * 50)

    print(f"\n  CPU Usage       : {cpu_pct:.1f}%"
          f"  [{cpu_status}]")
    print(f"    Threshold       : {CPU_THRESHOLD}%")

    print(f"\n  Memory Usage    : {mem_pct:.1f}%"
          f"  [{mem_status}]")
    print(f"    Used / Total    : {mem_used:.2f} GB / {mem_total:.2f} GB")
    print(f"    Threshold       : {MEMORY_THRESHOLD}%")

    print(f"\n  Disk Usage      : {disk_pct:.1f}%"
          f"  [{disk_status}]")
    print(f"    Used / Total    : {disk_used:.2f} GB / {disk_total:.2f} GB")
    print(f"    Threshold       : {DISK_THRESHOLD}%")

    print("\n" + "=" * 50)

    # ── Overall verdict ───────────────────────────────────────────────────────
    alerts = [m for m, pct, thr in [
        ("CPU",    cpu_pct,  CPU_THRESHOLD),
        ("Memory", mem_pct,  MEMORY_THRESHOLD),
        ("Disk",   disk_pct, DISK_THRESHOLD),
    ] if pct >= thr]

    if alerts:
        print(f"  ⚠  ACTION NEEDED: High usage on {', '.join(alerts)}")
    else:
        print("  ✓  All systems are running healthy.")

    print("=" * 50)


if __name__ == "__main__":
    print_report()
