// shopzafra.com — founding-list reservation capture
// POST /reserve {name, email, product, quantity?, list}
// Writes to the fleet Supabase `site_leads` table (same list as the founding list),
// tagged: site=shopzafra.com, track=founding-list, source=reserve-form, interest=product ×qty.

const PRODUCTS = new Set([
  'House Blend',
  'Estate Natural',
  'Estate Honey',
  'Harvest Subscription',
  'Reserve Lot Inquiry'
]);

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
  });

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  });
}

export async function onRequestPost({ request, env }) {
  let data;
  try {
    data = await request.json();
  } catch {
    return json({ ok: false, error: 'bad_json' }, 400);
  }

  const name = String(data.name || '').trim().slice(0, 120);
  const email = String(data.email || '').trim().toLowerCase().slice(0, 160);
  const product = String(data.product || '').trim().slice(0, 60);
  const quantity = data.quantity ? Math.min(99, Math.max(1, parseInt(data.quantity, 10) || 1)) : null;

  if (!name || name.length < 2) return json({ ok: false, error: 'name_required' }, 400);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ ok: false, error: 'email_invalid' }, 400);
  if (!PRODUCTS.has(product)) return json({ ok: false, error: 'product_unknown' }, 400);
  if (data.honeypot) return json({ ok: true }); // bot trap

  const interest = quantity ? `${product} x${quantity}` : product;

  const row = {
    site: 'shopzafra.com',
    track: 'founding-list',
    name,
    email,
    interest,
    source: 'reserve-form',
    status: 'new',
    session_id: crypto.randomUUID(),
    venture_slug: 'zafra',
    page_url: new URL(request.url).origin
  };

  const url = (env.SUPABASE_URL || '').replace(/\/$/, '');
  const key = env.SUPABASE_SVC_KEY;
  if (!url || !key) return json({ ok: false, error: 'not_configured' }, 500);

  const r = await fetch(`${url}/rest/v1/site_leads`, {
    method: 'POST',
    headers: {
      'apikey': key,
      'Authorization': `Bearer ${key}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=minimal'
    },
    body: JSON.stringify(row)
  });

  if (!r.ok) return json({ ok: false, error: 'insert_failed' }, 502);
  return json({ ok: true });
}
