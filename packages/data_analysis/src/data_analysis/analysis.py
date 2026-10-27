from pathlib import Path
import asyncio
import os

import dotenv
import pandas as pd
from sqlalchemy import create_engine, text

from data_analysis.client import LangsmithClient, load_langsmith_client
from data_analysis.thread_stats import ThreadStats

OUTPUT_DIR = Path("analysis_outputs")
SUMMARY_PATH = OUTPUT_DIR / "thread_usage_summary.csv"

EMAIL_PATTERN = r"me\_%"

MAX_CONCURRENT_REQUESTS = 10


USERS_QUERY = text(r"""
SELECT id, email
FROM "user"
WHERE email LIKE :email_pattern ESCAPE '\';
""")

THREADS_QUERY = text(r"""
SELECT
    t.id AS thread_id,
    u.email,
    t.user_id
FROM thread AS t
JOIN "user" AS u ON u.id = t.user_id
WHERE u.email LIKE :email_pattern ESCAPE '\'
ORDER BY u.email, t.created_at;
""")




def get_target_users_and_threads(engine):
    params = {"email_pattern": EMAIL_PATTERN}

    with engine.connect() as connection:
        users = pd.read_sql(USERS_QUERY, connection, params=params)
        threads = pd.read_sql(THREADS_QUERY, connection, params=params)

    return users, threads


async def summarize_thread(thread, client, stats, semaphore):
    async with semaphore:
        thread_data = await client.get_thread(str(thread.thread_id))
        usage = stats.summarize_thread_usage(thread_data)

    return {
        "user_id": thread.user_id,
        "email": thread.email,
        "thread_id": thread.thread_id,
        **usage,
    }


async def summarize_threads(threads, client):
    stats = ThreadStats()
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    rows = await asyncio.gather(
        *[
            summarize_thread(thread, client, stats, semaphore)
            for thread in threads.itertuples(index=False)
        ]
    )
    return pd.DataFrame(rows)


def write_analysis_outputs(summary):
    OUTPUT_DIR.mkdir(exist_ok=True)
    summary.to_csv(SUMMARY_PATH, index=False)
    return SUMMARY_PATH


async def main():
    engine = load_db_engine()
    client = load_langsmith_client()

    users, threads = get_target_users_and_threads(engine)

    print(f"Found {len(users)} users matching {EMAIL_PATTERN}")
    print(f"Found {len(threads)} threads for those users")

    summary = await summarize_threads(threads, client)
    output_path = write_analysis_outputs(summary)

    print(f"Wrote thread usage summary to {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
