// zafratrading.com — click tracking.
// POST /track {event:'click', box, hero, source, utm_*, referrer, page_url, session_id}
// Writes one row to the fleet Supabase `site_events` table. Signups are recorded by /signup itself.

import { SITE, VENTURE_SLUG, json, allowedOrigin, readJson, insertRow, configured, trackingFields } from './_lib/leads.js';

const EVENTS = new Set(['click']);

export async function onRequestOptions({ request, env }) {
  const { cors } = allowedOrigin(request, env);
  return new Response(null, { status: 204, headers: cors });
}

export async function onRequestPost({ request, env }) {
  const origin = allowedOrigin(request, env);
  if (!origin.ok) return json({ ok: false, error: 'forbidden' }, 403);

  const data = await readJson(request, 4096);
  if (!data) return json({ ok: false, error: 'bad_request' }, 400);
  if (!EVENTS.has(String(data.event || ''))) return json({ ok: false, error: 'event_unknown' }, 400);
  if (!configured(env)) return json({ ok: false, error: 'not_configured' }, 500);

  const ok = await insertRow(env, 'site_events', {
    ...trackingFields(data),
    site: SITE,
    venture_slug: VENTURE_SLUG,
    event: 'click'
  });
  console.log(`[track] click box=${data.box} hero=${data.hero} source=${data.utm_source || data.referrer || 'direct'} saved=${ok}`);
  return ok ? json({ ok: true }) : json({ ok: false, error: 'insert_failed' }, 502);
}
