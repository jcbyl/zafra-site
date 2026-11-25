// Shared helpers for the zafratrading.com lead + tracking functions.
// No secret is ever exposed to the page: Supabase + mail credentials live only in Pages env vars.

export const SITE = 'zafratrading.com';
export const VENTURE_SLUG = 'coffee';

export const HEROES = new Set(['hero-A', 'hero-B', 'hero-C', 'hero-NA']);
export const BOXES = new Set(['doors-founding', 'doors-wholesale', 'footer-founding']);

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }
  });

const CORS = {
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
};

// Only our own origin may post. The header is optional (non-browser clients), but if present it must be ours.
export function allowedOrigin(request, env) {
  const origin = request.headers.get('origin');
  if (!origin) return { ok: true, cors: CORS };
  const hosts = [`https://${SITE}`, `https://www.${SITE}`];
  const preview = (env.PREVIEW_ORIGIN || '').split(',').map((s) => s.trim()).filter(Boolean);
  const isPreview = /^https:\/\/[a-z0-9-]+\.zafra-site\.pages\.dev$/.test(origin);
  if (isPreview || hosts.concat(preview).includes(origin)) return { ok: true, cors: { ...CORS, 'Access-Control-Allow-Origin': origin } };
  return { ok: false, cors: CORS };
}

export async function readJson(request, maxBytes = 8192) {
  const len = Number(request.headers.get('content-length') || 0);
  if (len > maxBytes) return null;
  const text = await request.text();
  if (text.length > maxBytes) return null;
  try {
    const data = JSON.parse(text);
    return data && typeof data === 'object' && !Array.isArray(data) ? data : null;
  } catch {
    return null;
  }
}

// String field: trimmed, control chars stripped, hard length cap. Missing → ''.
export function str(v, max = 160) {
  if (typeof v !== 'string') return '';
  return v.replace(/[\u0000-\u001f\u007f]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, max);
}

export function oneOf(v, set, fallback = '') {
  const s = str(v, 40);
  return set.has(s) ? s : fallback;
}

export const validEmail = (e) => EMAIL_RE.test(e);

// Tracking context shared by clicks and signups: headline variant, box, source, campaign tags.
// source = the site that sent the visitor (campaign tag first, then referrer host, then 'direct').
export function trackingFields(data) {
  const utmSource = str(data.utm_source, 120);
  const utmMedium = str(data.utm_medium, 120);
  const utmCampaign = str(data.utm_campaign, 120);
  let referrer = str(data.referrer, 300);
  let refHost = '';
  if (referrer) {
    try {
      const u = new URL(referrer);
      if (u.protocol === 'http:' || u.protocol === 'https:') {
        refHost = u.hostname.replace(/^www\./, '');
        if (refHost === SITE || refHost === `www.${SITE}`) referrer = '';
      } else referrer = '';
    } catch {
      referrer = '';
    }
  }
  const source = utmSource || refHost || 'direct';
  let pageUrl = str(data.page_url, 300);
  try {
    const u = new URL(pageUrl);
    pageUrl = `${u.origin}${u.pathname === '/' ? '/' : u.pathname.replace(/\/$/, '')}`;
  } catch {
    pageUrl = `https://${SITE}/`;
  }
  return {
    hero_variant: oneOf(data.hero, HEROES, 'hero-NA'),
    box: oneOf(data.box, BOXES),
    source,
    utm_source: utmSource,
    utm_medium: utmMedium,
    utm_campaign: utmCampaign,
    referrer,
    page_url: pageUrl,
    session_id: str(data.session_id, 64).replace(/[^a-zA-Z0-9-]/g, '') || crypto.randomUUID()
  };
}

// Service-role insert through PostgREST. Resolves true/false, never throws.
export async function insertRow(env, table, row) {
  const url = (env.SUPABASE_URL || '').replace(/\/$/, '');
  const key = env.SUPABASE_SVC_KEY;
  if (!url || !key) return false;
  try {
    const r = await fetch(`${url}/rest/v1/${table}`, {
      method: 'POST',
      headers: {
        apikey: key,
        Authorization: `Bearer ${key}`,
        'Content-Type': 'application/json',
        Prefer: 'return=minimal'
      },
      body: JSON.stringify(row)
    });
    return r.ok;
  } catch {
    return false;
  }
}

export function configured(env) {
  return Boolean(env.SUPABASE_URL && env.SUPABASE_SVC_KEY);
}
