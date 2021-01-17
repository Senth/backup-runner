# ————————————————————————————
#       Backup Locations
# ————————————————————————————
# !!! The paths supports use of * and ** !!!
# /home/username/* -> Includes all files and dirs except those starting with dot .
# /home/username/.* -> Includes all files and dirs starting with dot .
# /home/**/*.py -> Includes all python files for all users

# Where the backups should be output to
BACKUP_DIR = "/mnt/backup"

# Days to keep old backups. By default this is set 65 days
# (optional)
# DAYS_TO_KEEP = 65

# Makes a daily full backup.
# (optional)
# DAILY_FULL = [
#   "/etc",
#   "/usr",
#   "/var",
# ]

# Use an alias for the saved backup (instead of daily_full)
# (optional)
# DAILY_ALIAS = "root"

# Makes a weekly full backup (makes the full backup on a Monday)
# Also makes daily diff backups.
# (optional)
# WEEKLY_FULL = [
#   "/home",
# ]

# Use an alias for the saved backup (instead of weekly_full)
# (optional)
# WEEKLY_ALIAS = "home"

# Makes a full backup the 1st every month.
# Also makes daily and weekly diff backups.
# (optional)
# MONTHLY_FULL = [
#   "/mnt/storage"
# ]

# Use an alias for the saved backup (instead of monthly_full)
# (optional)
# MONTHLY_ALIAS = "media"


# ————————————————————————————
#            MySQL
# ————————————————————————————

# MySQL backup username account for taking daily backups of the MySQL server
# Only works if MYSQL_USERNAME and MYSQL_PASSWORD both are set.
# (optional)
# MYSQL_USERNAME = "backup_user"
# MYSQL_PASSWORD = "sotetc*$+N"

# Change the default MySQL location which is localhost:3306
# (optional)
# MYSQL_ADDRESS = "localhost"
# MYSQL_PORT = 3306


# ————————————————————————————
#       EMAIL WARNINGS
# ————————————————————————————

# The email to mail warnings about full disk or failed backups.
# For this to work you have to setup so sendmail on your server.
# (optional)
# EMAIL_FROM = "this.server@gdomain.com"
# EMAIL_TO = "your.email@gmail.com"

# When to warn when the backup disk is almost full.
# By default it warns at 85% full
# WARN_FULL_PERCENTAGE = 85
