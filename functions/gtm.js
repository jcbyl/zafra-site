// GET /gtm.js — loads the Google Tag Manager container named in GTM_CONTAINER_ID (Pages env var).
// The container id stays out of the page code: when the variable is not set this serves an empty script.
const PATTERN = /^GTM-[A-Z0-9]{4,10}$/;

export async function onRequestGet({ env }) {
  const id = String(env.GTM_CONTAINER_ID || '').trim().toUpperCase();
  const js = PATTERN.test(id)
    ? `(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':Date.now(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','${id}');`
    : '/* Google Tag Manager: no container set on this site */';
  return new Response(js, {
    headers: {
      'Content-Type': 'application/javascript; charset=utf-8',
      'Cache-Control': 'no-store'
    }
  });
}
