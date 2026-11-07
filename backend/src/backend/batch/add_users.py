"""Create users or reset existing passwords from a file of email addresses."""

import argparse
import asyncio
from collections import Counter
from pathlib import Path
from backend.storage.models import File
from pydantic import EmailStr, TypeAdapter, ValidationError


async def run(path: Path, apply: bool) -> int:
    """Validate input, process each unique email, and report totals."""
    lines = (await asyncio.to_thread(path.read_text, encoding="utf-8-sig")).splitlines()
    validate_email = TypeAdapter(EmailStr)
    counts: Counter[str] = Counter()
    emails: list[str] = []
    seen: set[str] = set()
    for number, line in enumerate(lines, start=1):
        value = line.strip()
        if not value or value.startswith("#"):
            continue
        try:
            email = str(validate_email.validate_python(value))
        except ValidationError:
            print(f"INVALID line {number}: {value}")
            counts["invalid"] += 1
            continue
        if email in seen:
            counts["duplicates"] += 1
            continue
        seen.add(email)
        emails.append(email)

    print(f"Mode: {'APPLY' if apply else 'DRY RUN'}")
    print(f"File: {await asyncio.to_thread(path.resolve)}")
    print(f"Unique valid emails: {len(emails)}")
    if emails:
        from backend.accounts import UserCreate
        from backend.accounts.services import AccountService
        from backend.database.config import open_session

        if apply:
            from backend.core.firebase import initialize_firebase_app

            initialize_firebase_app()
        for email in emails:
            try:
                with open_session() as session:
                    accounts = AccountService(session)
                    existing = await accounts.get_account_by_email(email=email)
                    if existing:
                        if apply:
                            accounts.reset_password(existing.id, new_password=email)
                            print(f"PASSWORD RESET: {email}")
                            counts["password_reset"] += 1
                        else:
                            print(f"WOULD RESET PASSWORD: {email}")
                            counts["would_reset_password"] += 1
                    elif not apply:
                        print(f"WOULD CREATE: {email}")
                        counts["would_create"] += 1
                    else:
                        await accounts.create_account(
                            data=UserCreate(
                                username=email, email=email, password=email
                            ),
                            force_password_reset=True,
                        )
                        print(f"CREATED: {email}")
                        counts["created"] += 1
            except Exception as exc:
                print(f"FAILED: {email}: {exc}")
                counts["failed"] += 1

    print("\nSummary")
    for label in (
        "created",
        "would_create",
        "password_reset",
        "would_reset_password",
        "duplicates",
        "invalid",
        "failed",
    ):
        print(f"  {label.replace('_', ' ')}: {counts[label]}")
    return 1 if counts["invalid"] or counts["failed"] else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create users or reset existing passwords from an email file."
    )
    parser.add_argument("file", type=Path, help="Path to the email text file")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create users and reset existing passwords; default is a dry run",
    )
    args = parser.parse_args()
    try:
        return asyncio.run(run(args.file, args.apply))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
