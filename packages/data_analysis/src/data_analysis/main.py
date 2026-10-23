from pathlib import Path
from langsmith import Client
import dotenv
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text
import asyncio
dotenv.load_dotenv()




OUTPUT_DIR = Path("eda_outputs")
SUMMARY_PATH = OUTPUT_DIR / "summary.txt"
EMAIL_PATTERN = r"me\_%"

USER_SEGMENT_LABELS = {
    "light": "Light (1-2 threads)",
    "moderate": "Moderate (3-8 threads)",
    "heavy": "Heavy (9+ threads)",
}


def classify_user(thread_count):
    if thread_count <= 2:
        return "light"
    if thread_count <= 8:
        return "moderate"
    return "heavy"


def write_section(lines, title, content=""):
    lines.append(f"\n{title}")
    lines.append("=" * len(title))
    if content is not None and str(content):
        lines.append(str(content))


def save_current_figure(filename):
    path = OUTPUT_DIR / filename
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()
    return path


dotenv.load_dotenv()
db_url = dotenv.get_key(".env", "DB_URL")

if not db_url:
    raise ValueError("DB_URL is not set in .env")

OUTPUT_DIR.mkdir(exist_ok=True)
engine = create_engine(db_url)

users_query = text(r"""
SELECT *
FROM "user"
WHERE email LIKE 'me\_%' ESCAPE '\';
""")

threads_query = text("""
    SELECT t.id, t.user_id
    FROM thread AS t
    JOIN "user" AS u ON u.id = t.user_id
    WHERE u.email LIKE :email_pattern ESCAPE '\\'
""")

messages_query = text("""
    SELECT m.id, m.thread_id, m.created_at
    FROM message AS m
    JOIN thread AS t ON t.id = m.thread_id
    JOIN "user" AS u ON u.id = t.user_id
    WHERE u.email LIKE :email_pattern ESCAPE '\\'
""")

params = {"email_pattern": EMAIL_PATTERN}

with engine.connect() as connection:
    users = pd.read_sql(users_query, connection, params=params)
    threads = pd.read_sql(threads_query, connection, params=params)
    messages = pd.read_sql(messages_query, connection, params=params)

summary_lines = []

write_section(summary_lines, "Filtered Users")
summary_lines.append(f"Email pattern: {EMAIL_PATTERN}")
summary_lines.append(f"Total filtered rows: {len(users)}")
summary_lines.append(f"Unique users: {users['id'].nunique()}")

threads_per_user = threads.groupby("user_id").size()
messages_per_thread = messages.groupby("thread_id").size()

write_section(summary_lines, "Threads Per User", threads_per_user.describe())
write_section(summary_lines, "Messages Per Thread", messages_per_thread.describe())

user_clusters = threads_per_user.apply(classify_user)
cluster_counts = user_clusters.value_counts().reindex(["light", "moderate", "heavy"], fill_value=0)
cluster_percentages = (cluster_counts / cluster_counts.sum() * 100).fillna(0)

write_section(summary_lines, "User Segments")
for segment, count in cluster_counts.items():
    summary_lines.append(
        f"{USER_SEGMENT_LABELS[segment]}: {count} users ({cluster_percentages[segment]:.1f}%)"
    )

single_turn = int((messages_per_thread == 1).sum())
multi_turn = int((messages_per_thread > 1).sum())

write_section(summary_lines, "Conversation Types")
summary_lines.append(f"Single-turn threads: {single_turn}")
summary_lines.append(f"Multi-turn threads: {multi_turn}")

messages["created_at"] = pd.to_datetime(messages["created_at"], errors="coerce")
messages = messages.dropna(subset=["created_at"])
messages["hour"] = messages["created_at"].dt.hour
messages["date"] = messages["created_at"].dt.date

messages_by_hour = messages.groupby("hour").size().reindex(range(24), fill_value=0)
messages_by_day = messages.groupby("date").size()

write_section(summary_lines, "Time-Based Activity")
if messages_by_hour.sum():
    peak_hour = int(messages_by_hour.idxmax())
    peak_count = int(messages_by_hour.max())
    summary_lines.append(f"Peak hour: {peak_hour:02d}:00 with {peak_count} messages")
else:
    summary_lines.append("No message timestamps available.")

graph_paths = []

plt.figure(figsize=(9, 5))
threads_per_user.hist(bins=30, color="#2f6f73", edgecolor="white")
plt.title("Thread Volume Per User")
plt.xlabel("Number of threads created by a user")
plt.ylabel("Number of users")
graph_paths.append(save_current_figure("threads_per_user_distribution.png"))

plt.figure(figsize=(9, 5))
messages_per_thread.hist(bins=30, color="#8a5a44", edgecolor="white")
plt.title("Message Volume Per Thread")
plt.xlabel("Number of messages in a thread")
plt.ylabel("Number of threads")
graph_paths.append(save_current_figure("messages_per_thread_distribution.png"))

plt.figure(figsize=(10, 5))
messages_by_hour.plot(kind="bar", color="#4f6d9a")
plt.title("Messages By Hour Of Day")
plt.xlabel("Hour of day")
plt.ylabel("Number of messages")
plt.xticks(rotation=0)
graph_paths.append(save_current_figure("messages_by_hour.png"))

plt.figure(figsize=(11, 5))
messages_by_day.plot(color="#7a6f3d", linewidth=2)
plt.title("Messages Over Time")
plt.xlabel("Date")
plt.ylabel("Number of messages")
graph_paths.append(save_current_figure("messages_over_time.png"))

plt.figure(figsize=(8, 5))
cluster_counts.rename(USER_SEGMENT_LABELS).plot(kind="bar", color=["#729b79", "#d0a85c", "#9f5f5f"])
plt.title("User Segments By Thread Activity")
plt.xlabel("User segment")
plt.ylabel("Number of users")
plt.xticks(rotation=20, ha="right")
graph_paths.append(save_current_figure("user_segments.png"))

write_section(summary_lines, "Saved Graphs")
summary_lines.extend(str(path) for path in graph_paths)

SUMMARY_PATH.write_text("\n".join(summary_lines).strip() + "\n", encoding="utf-8")

print(f"Wrote summary to {SUMMARY_PATH}")
print(f"Saved {len(graph_paths)} graphs to {OUTPUT_DIR}")
