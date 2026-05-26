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
| x0 framework | Follow [x0 INSTALL.md](https://github.com/WEBcodeX1/x0/blob/main/INSTALL.md) |
| PostgreSQL ≥ 14 | Shared with x0 |
| Python ≥ 3.10 | `requests`, `psycopg2`, `pgdbpool`, `python-micro-esb` |
| GitHub Personal Access Token | Needs `repo` scope for private repos, `public_repo` for public |
| Stackfield API token | See Stackfield workspace settings → Integrations → API |

---

## Installation

### 1. Set up x0

Follow the official x0 installation guide to get the base framework running with PostgreSQL.

### 2. Install Python dependencies

```bash
pip install requests psycopg2-binary pgdbpool
pip install git+https://github.com/clauspruefer/python-micro-esb.git
```

### 3. Run database setup scripts

Connect to your x0 PostgreSQL database and execute the scripts in order:

```bash
psql -U postgres -d x0 -f database/01-create-schema.sql
psql -U postgres -d x0 -f database/02-insert-config.sql
psql -U postgres -d x0 -f database/03-insert-text.sql
```

### 4. Deploy static files

Copy the `static/` directory so it is served at `/static/github2sf/`:

```bash
cp -r static/ /var/www/x0/static/github2sf/
```

### 5. Deploy Python backend

Copy the `python/` directory into the x0 Python directory:

```bash
cp python/*.py /var/www/x0/python/github2sf/
```

### 6. Configure Apache2

Add the WSGI aliases from `docker/apache2.conf` to your Apache virtual host, then reload:

```bash
apache2ctl graceful
```

### 7. Open the application

Navigate to `http://your-server/?appid=github2sf` in your browser.

---

## Docker (quick start)

```bash
cd docker
docker compose up --build
```

Then open [http://localhost:8080/?appid=github2sf](http://localhost:8080/?appid=github2sf).

> **Note:** The Docker image fetches x0 and python-micro-esb from GitHub at build time.  
> You still need to run the database SQL scripts against the PostgreSQL container:
>
> ```bash
> docker exec -i github2sf-db psql -U postgres -d x0 < database/01-create-schema.sql
> docker exec -i github2sf-db psql -U postgres -d x0 < database/02-insert-config.sql
> docker exec -i github2sf-db psql -U postgres -d x0 < database/03-insert-text.sql
> ```

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
│   ├── Dockerfile
│   ├── docker-compose.yml
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
