#!/bin/bash
# organizer.sh - archives grades.csv with a timestamp and logs the action

SOURCE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# Stop with a clear message if there is nothing to archive
if [ ! -f "$SOURCE" ]; then
    echo "Error: $SOURCE not found in $(pwd). Run this script from the folder that contains it." >&2
    exit 1
fi

# Create the archive directory if it does not exist
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR" || { echo "Error: could not create $ARCHIVE_DIR" >&2; exit 1; }
    echo "Created directory: $ARCHIVE_DIR"
fi

# Build the timestamped name, e.g. grades_20251105-170000.csv
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"

# Move and rename in one step
if ! mv "$SOURCE" "$ARCHIVE_DIR/$ARCHIVED_NAME"; then
    echo "Error: failed to move $SOURCE to $ARCHIVE_DIR/$ARCHIVED_NAME" >&2
    exit 1
fi

# Reset the workspace with a new empty grades.csv
: > "$SOURCE"

# Append to the log (>> keeps entries from every run)
echo "[$TIMESTAMP] Original: $SOURCE | Archived as: $ARCHIVE_DIR/$ARCHIVED_NAME" >> "$LOG_FILE"

echo "Archived $SOURCE as $ARCHIVE_DIR/$ARCHIVED_NAME"
echo "Created new empty $SOURCE and logged to $LOG_FILE"
