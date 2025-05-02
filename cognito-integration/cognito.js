const COGNITO_DOMAIN = 'https://<your-cognito-domain>.auth.<aws-region>.amazoncognito.com';
const CLIENT_ID = 'your-client-id';
const REDIRECT_URI = window.location.origin;

function redirectToLogin() {
  const loginUrl = `${COGNITO_DOMAIN}/login?client_id=${CLIENT_ID}&response_type=code&scope=openid&redirect_uri=${encodeURIComponent(REDIRECT_URI)}`;
  window.location.href = loginUrl;
}

// Expose to other scripts
window.Auth = {
  redirectToLogin,
  COGNITO_DOMAIN,
  CLIENT_ID,
  REDIRECT_URI
};

handleRedirectCallback().then(() => {
  const idToken = sessionStorage.getItem('wuxia_id_token');

  if (!idToken) {
    Auth.redirectToLogin();
  }
});

async function handleRedirectCallback() {
  const params = new URLSearchParams(window.location.search);
  const code = params.get('code');
  if (!code) return;

  const tokenUrl = `${COGNITO_DOMAIN}/oauth2/token`;
  const body = new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: CLIENT_ID,
    code: code,
    redirect_uri: REDIRECT_URI
  });

  try {
    const response = await fetch(tokenUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body
    });

    const data = await response.json();
    sessionStorage.setItem('wuxia_id_token', data.id_token);
    sessionStorage.setItem('wuxia_access_token', data.access_token);
    window.history.replaceState({}, document.title, REDIRECT_URI);

  } catch (err) {
    console.error('Authentication failed:', err);
    Auth.redirectToLogin();
  }
}
