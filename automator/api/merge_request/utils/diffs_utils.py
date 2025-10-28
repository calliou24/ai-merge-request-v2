
def extract_section(text, start_tag, end_tag):
    """Extract text between two markers safely using split."""
    try:
        return text.split(start_tag, 1)[1].split(end_tag, 1)[0].strip()
    except IndexError:
        return None  # In case tags are missing


def truncate_diff(diff_text: str, max_lines: int = 50) -> str:
    """Keep full diff if small, otherwise truncate with context"""
    if not diff_text:
        return ""

    lines = diff_text.split("\n")
    if len(lines) <= max_lines:
        return diff_text

    # Keep first max_lines/2 and last max_lines/2 lines to preserve context
    half = max_lines // 2
    truncated = (
        lines[:half]
        + [f"\n... ({len(lines) - max_lines} lines omitted) ...\n"]
        + lines[-half:]
    )
    return "\n".join(truncated)


def Build_optimized_diffs(compare):
    return {
        "commits": [
            {
                "message": commit["message"],
                "author": commit["author_name"],
                "timestamp": commit["created_at"],
            }
            for commit in compare["commits"]
        ],
        "files_changed": [
            {
                "path": diff["new_path"],
                "status": (
                    "deleted"
                    if diff["deleted_file"]
                    else "new" if diff["new_file"] else "modified"
                ),
                "additions": diff.get("diff", "").count("\n+"),
                "deletions": diff.get("diff", "").count("\n-"),
                "diff": truncate_diff(diff.get("diff", "")),
            }
            for diff in compare["diffs"]
        ],
        "total_commits": len(compare["commits"]),
        "total_files": len(compare["diffs"]),
    }