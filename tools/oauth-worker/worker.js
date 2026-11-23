// Sign-in gateway for the AACM admin page (a Cloudflare Worker, free plan).
// It lets Decap CMS sign an admin in with their GitHub account. It stores nothing.
//
// Settings (Cloudflare > Worker > Settings > Variables):
//   GITHUB_CLIENT_ID      from the GitHub OAuth app
//   GITHUB_CLIENT_SECRET  from the GitHub OAuth app (add as a Secret)
//   SITE_ORIGIN           https://chicagoasanteman.org

const GITHUB_AUTHORIZE = 'https://github.com/login/oauth/authorize';
const GITHUB_TOKEN = 'https://github.com/login/oauth/access_token';

function randomState() {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return [...bytes].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function cookie(request, name) {
  const match = (request.headers.get('Cookie') || '').match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
  return match ? match[1] : '';
}

function page(env, message, ok) {
  const origin = JSON.stringify(env.SITE_ORIGIN);
  const payload = JSON.stringify(
    (ok ? 'authorization:github:success:' : 'authorization:github:error:') + JSON.stringify(message)
  ).replace(/</g, '\\u003c');
  const body = `<!doctype html><meta charset="utf-8"><title>Signing in</title><p>Signing you in...</p>
<script>
(function () {
  var origin = ${origin};
  function receive(e) {
    if (e.origin !== origin) return;
    window.opener.postMessage(${payload}, e.origin);
    window.removeEventListener('message', receive, false);
    window.close();
  }
  window.addEventListener('message', receive, false);
  window.opener.postMessage('authorizing:github', origin);
})();
</script>`;
  return new Response(body, {
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Set-Cookie': 'oauth_state=; Max-Age=0; Path=/; Secure; HttpOnly; SameSite=Lax',
    },
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/auth') {
      const state = randomState();
      const params = new URLSearchParams({
        client_id: env.GITHUB_CLIENT_ID,
        redirect_uri: url.origin + '/callback',
        // public_repo is enough because the site's repository is public.
        scope: 'public_repo',
        state,
      });
      return new Response(null, {
        status: 302,
        headers: {
          Location: GITHUB_AUTHORIZE + '?' + params,
          'Set-Cookie': 'oauth_state=' + state + '; Max-Age=600; Path=/; Secure; HttpOnly; SameSite=Lax',
        },
      });
    }

    if (url.pathname === '/callback') {
      const code = url.searchParams.get('code');
      const state = url.searchParams.get('state');
      if (!code || !state || state !== cookie(request, 'oauth_state')) {
        return page(env, { message: 'Sign-in could not be checked. Close this window and try again.' }, false);
      }
      const res = await fetch(GITHUB_TOKEN, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json', 'User-Agent': 'aacm-admin-sign-in' },
        body: JSON.stringify({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code,
          redirect_uri: url.origin + '/callback',
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!data.access_token) {
        return page(env, { message: 'GitHub did not sign you in. Close this window and try again.' }, false);
      }
      return page(env, { token: data.access_token, provider: 'github' }, true);
    }

    return new Response('AACM admin sign-in is running.', { status: 200 });
  },
};
