-- Schema for bbtrio-clone session archive.
-- Run this once in Supabase SQL Editor after creating the project.
--
-- Multi-tenant by device_id only (no auth). Each device generates a UUID
-- on first launch and stores it in localStorage; the same UUID is sent
-- with every read and write as the x-device-id HTTP header. RLS makes
-- sure one device can only read its own rows.

create extension if not exists pgcrypto;

create table if not exists public.sessions (
  id            uuid primary key default gen_random_uuid(),
  device_id     text not null,
  category      text not null,                -- Standard | Advanced | Expert
  puzzle_date   date not null,                -- the in-game date the puzzle was for
  total_ms      integer,                      -- accumulatedMs at sync time
  undo_count    integer,
  finished_at   timestamptz,                  -- null while in progress
  data          jsonb not null,               -- full snapshot (state, moveLog, etc.)
  created_at    timestamptz not null default now()
);

create index if not exists sessions_device_idx
  on public.sessions (device_id, created_at desc);
create index if not exists sessions_date_idx
  on public.sessions (puzzle_date);

alter table public.sessions enable row level security;

-- Helper: pull x-device-id out of the PostgREST request.headers JSON.
create or replace function public.current_device_id() returns text
language sql stable as $$
  select nullif(current_setting('request.headers', true)::json ->> 'x-device-id', '')
$$;

drop policy if exists "anon write own" on public.sessions;
create policy "anon write own"
  on public.sessions
  for insert
  to anon
  with check (device_id = public.current_device_id());

drop policy if exists "anon read own" on public.sessions;
create policy "anon read own"
  on public.sessions
  for select
  to anon
  using (device_id = public.current_device_id());

-- Optional, useful later: allow anon to delete own rows (for "wipe my data"
-- buttons). Comment out if you want strictly append-only history.
drop policy if exists "anon delete own" on public.sessions;
create policy "anon delete own"
  on public.sessions
  for delete
  to anon
  using (device_id = public.current_device_id());
