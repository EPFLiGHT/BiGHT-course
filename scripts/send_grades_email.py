#!/usr/bin/env python3
"""Email graded quiz PDFs to students, either via Microsoft Graph or as
ready-to-send .eml drafts for Outlook.

=====================================================================
 TWO WAYS TO SEND -- pick whichever fits
=====================================================================
1. --eml-dir: generates one .eml file per student, with the subject,
   body and PDF attachment already filled in. No Azure setup, no
   OAuth, nothing to configure below -- just open each file (Outlook
   loads it as an editable draft, not a received message, since it
   carries no delivery headers) and click Send. You do the sending,
   one click per student, using whatever mailbox Outlook is already
   signed into.

2. --send / --test-only: fully automated sending via Microsoft Graph,
   signing in as you through your browser. Faster for a whole class,
   but needs the one-time Azure app registration below first.

=====================================================================
 ONE-TIME SETUP -- only needed for --send / --test-only, not --eml-dir
=====================================================================
This mode signs in as *you* (via your browser, with your EPFL
credentials) and sends mail through Microsoft Graph's ``/me/sendMail``
delegated endpoint -- so emails come from your own EPFL address, land
in your own Sent Items, and never need a stored password.

To do that, Microsoft Graph requires an "app registration" (a
client ID) that requests the ``Mail.Send`` delegated permission:

1. Go to https://portal.azure.com (sign in with your EPFL account) ->
   "Azure Active Directory" / "Microsoft Entra ID" -> "App registrations"
   -> "New registration".
     - Name: anything, e.g. "BiGHT grade mailer".
     - Supported account types: "Accounts in this organizational
       directory only (EPFL)".
     - Redirect URI: platform "Mobile and desktop applications",
       URI ``http://localhost``.
2. Copy the "Application (client) ID" from the app's Overview page
   into CLIENT_ID below.
3. Under "API permissions" -> "Add a permission" -> "Microsoft Graph"
   -> "Delegated permissions" -> add ``Mail.Send``.
4. If your account can't self-consent (EPFL's tenant may require
   this), ask EPFL IT (the Service Desk) to grant admin consent for
   the app, or to register it for you and share the client ID.

If step 1 is blocked by EPFL policy for your account, this is the
one thing only EPFL IT can unblock -- there's no way around it from
this script, since Microsoft Graph requires a registered app for any
delegated-permission sign-in.

This setup happens once; every later run just re-authenticates
against the same app (and after the first browser sign-in, MSAL's
local token cache lets most re-runs skip the browser entirely).

=====================================================================
 EDITING THE EMAIL
=====================================================================
Change SUBJECT and BODY below directly -- they're plain Python
strings, formatted with {first_name}, {last_name}, {sciper},
{quiz_number} and {score} for each student.

=====================================================================
 USAGE
=====================================================================
    python3 scripts/send_grades_email.py 1                        # dry run: prints what would be sent
    python3 scripts/send_grades_email.py 1 --eml-dir DIR           # write one .eml draft per student to DIR
    python3 scripts/send_grades_email.py 1 --test-only me@epfl.ch  # send ONE real test email to yourself (Graph)
    python3 scripts/send_grades_email.py 1 --send                  # actually email the whole class (Graph)

Always dry-run first. For --send, try --test-only on yourself before
mailing the whole class -- there is no "unsend".
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Edit these for each mailing.
# ---------------------------------------------------------------------------
SUBJECT = "BiGHT Quiz {quiz_number} -- your grade and scanned copy"
BODY = """Dear {first_name},

Please find attached your corrected copy for BiGHT Quiz {quiz_number}.
The scan is included as a PDF file.

Your score: {score}/16

Best regards,
The BiGHT team
"""

# ---------------------------------------------------------------------------
# One-time Azure AD app registration -- see the setup instructions above.
# ---------------------------------------------------------------------------
CLIENT_ID = ""  # "Application (client) ID" from the Azure AD app registration
TENANT_ID = "epfl.ch"  # EPFL's tenant; a tenant GUID also works

CONTACTS_CSV = Path("quiz-drafts/contacts/students_contacts.csv")
SCIPER_COLUMN = "Numéro d’identification"  # curly apostrophe, matches the exported CSV
GRAPH_SEND_MAIL = "https://graph.microsoft.com/v1.0/me/sendMail"
SCOPES = ["Mail.Send"]
TOKEN_CACHE_PATH = Path.home() / ".cache" / "bight-mail-token-cache.json"


def load_contacts(csv_path: Path) -> dict[str, dict[str, str]]:
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return {
            row[SCIPER_COLUMN].strip(): {
                "first_name": row["Prénom"].strip(),
                "last_name": row["Nom de famille"].strip(),
                "email": row["Adresse de courriel"].strip(),
            }
            for row in reader
        }


def load_scores(results_dir: Path, quiz_number: str) -> dict[str, str]:
    csv_path = results_dir / "grades" / f"moodle_export_quiz{quiz_number}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(
            f"{csv_path} not found -- run amc_grade_scan.py for this quiz first."
        )
    with csv_path.open(encoding="utf-8", newline="") as handle:
        return {row["SCIPER"]: row["Total"] for row in csv.DictReader(handle)}


def get_access_token() -> str:
    import msal

    if not CLIENT_ID:
        raise RuntimeError(
            "CLIENT_ID is empty -- see the setup instructions in this script's docstring."
        )

    TOKEN_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    cache = msal.SerializableTokenCache()
    if TOKEN_CACHE_PATH.exists():
        cache.deserialize(TOKEN_CACHE_PATH.read_text(encoding="utf-8"))

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        token_cache=cache,
    )
    accounts = app.get_accounts()
    result = app.acquire_token_silent(SCOPES, account=accounts[0]) if accounts else None
    if not result:
        # Opens your default browser to EPFL's Microsoft sign-in page.
        result = app.acquire_token_interactive(scopes=SCOPES)

    if cache.has_state_changed:
        TOKEN_CACHE_PATH.write_text(cache.serialize(), encoding="utf-8")

    if "access_token" not in result:
        raise RuntimeError(
            f"Authentication failed: {result.get('error_description', result)}"
        )
    return result["access_token"]


def build_message(
    to_email: str, subject: str, body: str, attachment_path: Path
) -> dict:
    import base64

    return {
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": to_email}}],
            "attachments": [
                {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": attachment_path.name,
                    "contentBytes": base64.b64encode(
                        attachment_path.read_bytes()
                    ).decode("ascii"),
                }
            ],
        },
        "saveToSentItems": "true",
    }


def send_email(token: str, message: dict) -> None:
    import requests

    response = requests.post(
        GRAPH_SEND_MAIL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=message,
        timeout=30,
    )
    if response.status_code != 202:
        raise RuntimeError(f"Send failed ({response.status_code}): {response.text}")


def write_eml(
    sciper: str,
    to_email: str,
    subject: str,
    body: str,
    attachment_path: Path,
    out_dir: Path,
) -> Path:
    """Writes a .eml draft: no delivery headers (Received, Message-ID from a
    server, etc.), so mail clients that open it -- Outlook included -- treat
    it as an unsent draft to edit and send, not a received message."""
    from email.message import EmailMessage

    message = EmailMessage()
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)
    message.add_attachment(
        attachment_path.read_bytes(),
        maintype="application",
        subtype="pdf",
        filename=attachment_path.name,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    eml_path = out_dir / f"{sciper}.eml"
    eml_path.write_bytes(bytes(message))
    return eml_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("quiz_number", help="Quiz number, e.g. 1")
    parser.add_argument(
        "--send",
        action="store_true",
        help="Actually send emails. Without this, only prints a dry run.",
    )
    parser.add_argument(
        "--only",
        metavar="SCIPER",
        action="append",
        help="Only include this student (repeatable). Useful for a single correction/resend after a rescan.",
    )
    parser.add_argument(
        "--test-only",
        metavar="EMAIL",
        help="Send a single real test email to this address instead of the whole class (still needs --send).",
    )
    parser.add_argument(
        "--eml-dir",
        type=Path,
        metavar="DIR",
        help="Write one .eml draft per student to DIR instead of sending via Graph. No Azure setup needed.",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        help="Defaults to quiz-drafts/quizzes/quiz<N>/results.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Seconds to wait between Graph sends, to avoid throttling.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    results_dir = (
        args.results_dir
        or Path("quiz-drafts") / "quizzes" / f"quiz{args.quiz_number}" / "results"
    )
    contacts = load_contacts(CONTACTS_CSV)
    scores = load_scores(results_dir, args.quiz_number)

    jobs: list[
        tuple[str, str, str, str, Path]
    ] = []  # (sciper, email, subject, body, pdf_path)
    for sciper, score in scores.items():
        contact = contacts.get(sciper)
        if not contact:
            print(
                f"WARNING: no contact found for SCIPER {sciper}, skipping.",
                file=sys.stderr,
            )
            continue
        pdf_path = results_dir / "pdfs" / f"{sciper}.pdf"
        if not pdf_path.exists():
            print(
                f"WARNING: missing PDF for SCIPER {sciper}, skipping.", file=sys.stderr
            )
            continue
        fields = {
            "quiz_number": args.quiz_number,
            "score": score,
            "sciper": sciper,
            **contact,
        }
        jobs.append(
            (
                sciper,
                contact["email"],
                SUBJECT.format(**fields),
                BODY.format(**fields),
                pdf_path,
            )
        )

    if args.only:
        wanted = set(args.only)
        jobs = [job for job in jobs if job[0] in wanted]
        missing = wanted - {job[0] for job in jobs}
        if missing:
            print(
                f"WARNING: --only SCIPER(s) not found among prepared jobs: {', '.join(sorted(missing))}",
                file=sys.stderr,
            )

    if args.test_only:
        if not jobs:
            print("No jobs to build a test email from.", file=sys.stderr)
            return
        sciper, _, subject, body, pdf_path = jobs[0]
        jobs = [(sciper, args.test_only, subject, body, pdf_path)]

    print(f"{len(jobs)} email(s) prepared for quiz {args.quiz_number}.")
    for _sciper, email, subject, _body, pdf_path in jobs:
        print(f"  -> {email}  [{subject}]  attachment={pdf_path.name}")

    if args.eml_dir:
        for sciper, email, subject, body, pdf_path in jobs:
            eml_path = write_eml(sciper, email, subject, body, pdf_path, args.eml_dir)
            print(f"Wrote {eml_path}")
        print(
            f"\n{len(jobs)} .eml draft(s) in {args.eml_dir} -- open each in Outlook and click Send."
        )
        return

    if not args.send:
        print(
            "\nDry run only -- nothing was sent. Re-run with --send to actually send, or --eml-dir to write Outlook drafts instead."
        )
        return

    token = get_access_token()
    for _sciper, email, subject, body, pdf_path in jobs:
        send_email(token, build_message(email, subject, body, pdf_path))
        print(f"Sent to {email}")
        time.sleep(args.delay)


if __name__ == "__main__":
    main()
