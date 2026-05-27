# github2stackfield

**github2stackfield** is an x0 web application that bridges **GitHub Issues** with **Stackfield Tasks**.  
It lets you search GitHub issues, inspect their details, and create corresponding Stackfield tasks — all from a clean, Bootstrap-styled browser frontend.

---

## Architecture

| Layer | Technology |
|---|---|
| Browser frontend | [x0 JavaScript framework](https://github.com/WEBcodeX1/x0) with Bootstrap default theme |
| Backend services | Python WSGI scripts via [python-micro-esb](https://github.com/clauspruefer/python-micro-esb) |
| Database | PostgreSQL (shared x0 instance) |
| Deployment | Apache2 + mod_wsgi (Docker or bare-metal) |

---

## Screens

### Screen 1 — User Credentials
Configure and verify API access for both platforms.

- **GitHub API Credentials** — enter your GitHub username and Personal Access Token.  
  Click *Verify GitHub Credentials* to validate and store them.
- **Stackfield API Credentials** — enter your Stackfield e-mail and API token.  
  Click *Verify Stackfield Credentials* to validate and store them.

### Screen 2 — Issue / Task Mapping
Search GitHub issues and select one to map to Stackfield.

1. Enter the target repository (`owner/repository`) and an optional search term.
2. Click **Search Issues** — results populate the issue list below.
3. Right-click any row and select **Connect Stackfield Task** to navigate to Screen 3.

### Screen 3 — Connect Stackfield Task
Review the selected GitHub issue and create a Stackfield task.

- **GitHub Issue Properties** — read-only fields: issue number, state, title, URL.
- **Stackfield Task Mapping** — editable fields pre-populated from the issue:
  - *Stackfield Room ID* — the target Stackfield room / channel identifier.
  - *Task Title* — editable, defaults to the GitHub issue title.
  - *Description* — editable, defaults to the GitHub issue body.
  - *Priority* — Low / Medium / High / Urgent.
- Click **Create New Stackfield Task** — a new task is created in Stackfield via the REST API.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Docker Engine | With Compose V2 (`docker compose`) |
| GitHub Personal Access Token | Needs `repo` scope for private repos, `public_repo` for public |
| Stackfield API token | See Stackfield workspace settings → Integrations → API |

---

## Docker (quick start)

The application uses the official x0 container images:

- **`ghcr.io/webcodex1/x0-app`** — Apache2 + mod_wsgi web application server with the x0 JavaScript framework pre-installed ([packages page](https://github.com/WEBcodeX1/x0/pkgs/container/x0-app))
- **`ghcr.io/webcodex1/x0-db`** — PostgreSQL 16 database with the x0 schema pre-installed ([packages page](https://github.com/WEBcodeX1/x0/pkgs/container/x0-db))

Both custom images are built automatically on `docker compose up --build`:

- `docker/Dockerfile` extends `ghcr.io/webcodex1/x0-app` and copies all static files, Python WSGI scripts, and the Apache2 config snippet into the image.
- `docker/Dockerfile.db` extends `ghcr.io/webcodex1/x0-db` and runs the github2stackfield SQL init scripts (`database/0*.sql`) against the x0 database on first start.

```bash
cd docker
docker compose up --build
```

Then open [http://localhost:8080/?appid=github2sf](http://localhost:8080/?appid=github2sf).

No further manual configuration is required.

---

## Project structure

```
github2stackfield/
├── static/
│   ├── menu.json         # x0 navigation menu definition
│   ├── object.json       # x0 UI objects (formfields, lists, buttons …)
│   └── skeleton.json     # x0 screen layout
├── python/
│   ├── service_implementation.py   # GitHubService + StackfieldService ClassHandlers
│   ├── user_routing.py             # python-micro-esb ServiceRouter routing functions
│   ├── VerifyGitHubCredentials.py  # WSGI – verify GitHub credentials
│   ├── VerifyStackfieldCredentials.py  # WSGI – verify Stackfield credentials
│   ├── SearchGitHubIssues.py       # WSGI – search issues, populate list
│   ├── GetGitHubIssueDetails.py    # WSGI – fetch issue details for Screen 3
│   ├── CreateStackfieldTask.py     # WSGI – create Stackfield task
│   ├── POSTData.py                 # x0 POST body reader helper
│   └── StdoutLogger.py            # logging helper
├── database/
│   ├── 01-create-schema.sql   # github2sf schema + tables
│   ├── 02-insert-config.sql   # x0 app configuration rows
│   └── 03-insert-text.sql     # UI text / i18n entries
├── docker/
│   ├── Dockerfile          # extends x0-app, bakes in static/ python/ apache2.conf
│   ├── Dockerfile.db       # extends x0-db, auto-inits github2sf schema on startup
│   ├── docker-compose.yml
│   ├── db-init.sh          # startup script used by Dockerfile.db
│   └── apache2.conf
└── README.md
```

---

## python-micro-esb integration

The backend services are built on the [python-micro-esb](https://github.com/clauspruefer/python-micro-esb) framework:

- **`service_implementation.py`** — contains `GitHubService` and `StackfieldService`, both subclassing `microesb.ClassHandler`.  Each class exposes service methods (`verify`, `search_issues`, `get_issue_details`, `create_task`).
- **`user_routing.py`** — routing functions consumed by `ServiceRouter.send()`.  Each function instantiates the appropriate service class, calls the relevant method, and returns the result.
- **WSGI scripts** — thin wrappers that read the x0 POST payload, call `ServiceRouter.send()`, and return JSON to the x0 frontend.

---

## Stackfield API notes

Stackfield's REST API is available at `https://www.stackfield.com/api/v1/`.  
Key endpoints used:

| Endpoint | Purpose |
|---|---|
| `GET /v1/user` | Verify credentials |
| `POST /v1/rooms/{room_id}/tasks` | Create a new task |

The **Room ID** can be found in Stackfield under *Room settings → General → Room ID* or via the URL slug.

---

## License

See [LICENSE](LICENSE).
