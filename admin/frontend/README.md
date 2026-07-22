# TeacherBot Admin Frontend

React + TypeScript admin panel for viewing and managing TeacherBot users, backed by the FastAPI service in [`admin/`](../).

## Stack

- **Vite** + **React** + **TypeScript**
- **React Router** — routing between the users list and user detail pages
- **TanStack Query** — data fetching, caching, and loading/error state
- **CSS Modules** — scoped component styles

## Pages

- `/users` — table of all users (ID, chat ID, name, total tokens, block status) with a link to each user's detail page
- `/users/:id` — user details, a Block/Unblock button, and a table of that user's messages

## Setup

```bash
npm install
cp .env.example .env   # set VITE_API_BASE_URL if the backend isn't on localhost:8000
npm run dev
```

The dev server runs on `http://localhost:5173`. It expects the FastAPI backend (see repo root README) to be running and reachable at `VITE_API_BASE_URL`.

## Scripts

- `npm run dev` — start the Vite dev server
- `npm run build` — type-check and build for production
- `npm run lint` — run Oxlint
- `npm run preview` — preview the production build locally
