// zafratrading.com — founding-list / wholesale signup capture.
// POST /signup {list, name, email, business?, location, message?, box, hero, source, utm_*, referrer, page_url, session_id, hp, ts}
//  1. saves the lead to the fleet Supabase `site_leads` table (venture_slug: coffee)
//  2. at the same moment mails the same details to info@zafratrading.com
//  3. records a 'signup' event in `site_events` for the tracking view
// Spam protection: honeypot field + minimum time-on-form. Both fail closed to a silent fake-ok.

import {
  SITE,
  VENTURE_SLUG,
  json,
  allowedOrigin,
  readJson,
  str,
  validEmail,
  insertRow,
  configured,
  trackingFields
} from './_lib/leads.js';

const MIN_FORM_MS = 2500; // bots post in milliseconds; a person whose browser autofills the form needs about this long to press the button
const MAX_FORM_MS = 2 * 60 * 60 * 1000;

export async function onRequestOptions({ request, env }) {
  const { cors } = allowedOrigin(request, env);
  return new Response(null, { status: 204, headers: cors });
}

export async function onRequestPost({ request, env }) {
  const origin = allowedOrigin(request, env);
  if (!origin.ok) return json({ ok: false, error: 'forbidden' }, 403);

  const data = await readJson(request);
  if (!data) return json({ ok: false, error: 'bad_request' }, 400);
  if (!configured(env)) return json({ ok: false, error: 'not_configured' }, 500);

  // Spam gate — honeypot filled, or form submitted too fast / too stale.
  const elapsed = Date.now() - (Number(data.ts) || 0);
  const bot = Boolean(str(data.hp, 200)) || (Number.isFinite(elapsed) && (elapsed < MIN_FORM_MS || elapsed > MAX_FORM_MS));

  const list = data.list === 'wholesale' ? 'wholesale' : data.list === 'founding' ? 'founding' : '';
  const track = trackingFields(data);
  const ctx = { ...track, site: SITE, venture_slug: VENTURE_SLUG };

  if (bot) return json({ ok: true }); // say nothing, store nothing

  const name = str(data.name, 120);
  const email = str(data.email, 160).toLowerCase();
  const business = str(data.business, 160);
  const location = str(data.location, 160);
  const message = str(data.message, 1000);
  const box = ctx.box || (list === 'wholesale' ? 'doors-wholesale' : 'doors-founding');
  const boxList = box === 'doors-wholesale' ? 'wholesale' : 'founding';

  if (!list) return json({ ok: false, error: 'list_unknown' }, 400);
  if (name.length < 2) return json({ ok: false, error: 'name_required' }, 400);
  if (!validEmail(email)) return json({ ok: false, error: 'email_invalid' }, 400);
  if (location.length < 2) return json({ ok: false, error: 'location_required' }, 400);
  if (list === 'wholesale' && business.length < 2) return json({ ok: false, error: 'business_required' }, 400);
  if (boxList !== list) return json({ ok: false, error: 'box_mismatch' }, 400);

  const row = {
    site: SITE,
    venture_slug: VENTURE_SLUG,
    track: list === 'wholesale' ? 'wholesale' : 'founding-list',
    name,
    email,
    company: list === 'wholesale' ? business : null,
    location,
    interest: list === 'wholesale' && message ? message : null,
    source: ctx.source,
    status: 'new',
    page_url: ctx.page_url,
    session_id: ctx.session_id,
    hero_variant: ctx.hero_variant,
    box,
    utm_source: ctx.utm_source || null,
    utm_medium: ctx.utm_medium || null,
    utm_campaign: ctx.utm_campaign || null,
    referrer: ctx.referrer || null
  };

  // Two independent routes — a lead is kept if either one goes through.
  const mail = {
    to: env.LEAD_MAIL_TO || `info@${SITE}`,
    from: env.LEAD_MAIL_FROM || '',
    clientId: env.MAIL_CLIENT_ID || '',
    clientSecret: env.MAIL_CLIENT_SECRET || '',
    tenantId: env.MAIL_TENANT_ID || ''
  };
  const [saved, mailed] = await Promise.all([
    saveLead(env, row),
    sendNotification(mail, row)
  ]);

  if (saved || mailed) {
    await insertRow(env, 'site_events', { ...ctx, event: 'signup' });
  }
  console.log(`[signup] ${row.track} box=${row.box} hero=${row.hero_variant} source=${row.source} saved=${saved} mailed=${mailed}`);
  if (!saved && !mailed) return json({ ok: false, error: 'failed' }, 502);
  return json({ ok: true });
}

// site_leads holds one lead per site and browser tab (unique on site + session_id).
// A visitor who signs up on a second list in the same tab keeps the tab id with a number after it.
async function saveLead(env, row) {
  let saved = await insertRow(env, 'site_leads', row);
  for (let n = 2; !saved && n <= 9; n++) {
    saved = await insertRow(env, 'site_leads', { ...row, session_id: `${row.session_id}-${n}` });
  }
  return saved;
}

// Date and time of signup, Puerto Rico time, for the email body.
function stamp() {
  return new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Puerto_Rico',
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date()) + ' AST';
}

let tokenCache = { token: '', exp: 0 };

async function graphToken({ clientId, clientSecret, tenantId }) {
  if (!clientId || !clientSecret || !tenantId) return '';
  if (tokenCache.token && tokenCache.exp > Date.now()) return tokenCache.token;
  const body = new URLSearchParams({
    grant_type: 'client_credentials',
    client_id: clientId,
    client_secret: clientSecret,
    scope: 'https://graph.microsoft.com/.default'
  });
  const r = await fetch(`https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body
  });
  if (!r.ok) return '';
  const j = await r.json();
  tokenCache = { token: j.access_token, exp: Date.now() + ((j.expires_in || 3600) - 120) * 1000 };
  return tokenCache.token;
}

// Mail the lead to info@zafratrading.com. Resolves true/false, never throws.
async function sendNotification(mail, row) {
  if (!mail.to || !mail.from) return false;
  const wholesale = row.track === 'wholesale';
  const subject = wholesale
    ? `Wholesale: ${row.company}, ${row.location} [${row.hero_variant}]`
    : `Founding list: ${row.name}, ${row.location} [${row.hero_variant}]`;
  const lines = [
    wholesale ? 'Wholesale inquiry' : 'Founding list signup',
    `Name: ${row.name}`,
    wholesale ? `Business: ${row.company}` : '',
    `Email: ${row.email}`,
    `Location: ${row.location}`,
    wholesale && row.interest ? `Volume and program: ${row.interest}` : '',
    '',
    `Box on page: ${row.box}`,
    `Headline variant: ${row.hero_variant}`,
    `Source: ${row.source}`,
    `Campaign: ${row.utm_source || '-'} / ${row.utm_medium || '-'} / ${row.utm_campaign || '-'}`,
    row.referrer ? `Sent by: ${row.referrer}` : '',
    `Page: ${row.page_url}`,
    `Signed up: ${stamp()}`
  ].filter((l) => l !== '');

  const payload = {
    message: {
      subject,
      body: { contentType: 'Text', content: lines.join('\n') },
      toRecipients: [{ emailAddress: { address: mail.to } }],
      replyTo: [{ emailAddress: { address: row.email } }]
    },
    saveToSentItems: false
  };

  try {
    const token = await graphToken(mail);
    if (!token) return false;
    const r = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(mail.from)}/sendMail`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return r.ok; // 202 Accepted
  } catch {
    return false;
  }
}
