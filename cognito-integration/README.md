# 🛡 Amazon Cognito Integration

Here we demonstrate how to integrate **Amazon Cognito** to protect your Wuxia Serverless Gen AI App via API Gateway, while ensuring unauthorized users are blocked (and redirected to login).

## ✅ Goal Recap

- Redirect unauthenticated users to a login page (hosted by Cognito).

- Use Cognito Authorizer in API Gateway to block non-authenticated access.

- Avoid code complexity — no custom JWT decoding, no additional edge protection.

---

## 📦 Architecture Overview

![Alt text](../images/architecture-cognito.png?raw=true "Architecture-Cognito")

---

## 🔐 Strategy: Use Cognito User Pool + Hosted UI + API Gateway Authorizer

### Set Up Cognito User Pool

- Create a Cognito User Pool
- Choose Single-Page-Application settings
- Enable email or username login
- Set your CloudFront distribution URL as return URL

![Alt text](../images/cognito-setup.png?raw=true "Architecture")


### Create at least one user for testing

- Go to your App client
- Jump to "View login page"
- Create a user.

![Alt text](../images/cognito-view-login-page.png?raw=true "View login page")

### Protect your API Gateway Using Cognito Authorizer

In your API Gateway:

- Go to Authorizers (left menu)
- Create a Cognito Authorizer
    - Set **Authorization type** value to **Authorization**

![Alt text](../images/cognito-create-autorizer.png?raw=true "Create Authorizer")

- In resource /generate, method POST, 
- Edit Method Request and set the **Authorization** to your Cognito Authorizer

![Alt text](../images/cognito-edit-method-request.png?raw=true "Edit method request")

This will ensure every request to your endpoint is blocked unless a valid token is provided.

- Deploy your API to the appropriate stage (prod or whatever you want to use)

### Handle Auth in Frontend (your current static site)

- If no token is present in localStorage/sessionStorage:

    - Redirect user to the Cognito Hosted UI login.

- Once logged in, Cognito redirects back with an authorization code.

- Use JavaScript to:

    - Exchange the authorization code for **ID token** + **access token** via Cognito’s /oauth2/token endpoint.

    - Store the **ID token** in sessionStorage.

The code is provided:
- cognito.js: new file to handle authentication process. **Make sure to set accordingly**:
  - const COGNITO_DOMAIN = 'https://**YOUR-COGNITO-DOMAIN**.auth.**AWS-REGION**.amazoncognito.com' 
  - const CLIENT_ID = '**YOUR-COGNITO-CLIENT-ID**'


```javascript
const COGNITO_DOMAIN = 'https://<your-cognito-domain>.auth.<aws-region>.amazoncognito.com';
const CLIENT_ID = '<your-client-id>';
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
```

- wuxia.js: updated function callApi to pass the ID token to the API Gateway

```javascript
function callApi(templateType) {
  const apiGatewayUrl = document.getElementById('apiGatewayUrl').value;
  const contentId = `${templateType}-content`;
  const temperatureId = `${templateType}-temperature`;
  const topPId = `${templateType}-topP`;
  
  const modelId = document.getElementById('modelSelector').value;
  const content = document.getElementById(contentId).value;
  const temperature = parseFloat(document.getElementById(temperatureId).value);
  const topP = parseFloat(document.getElementById(topPId).value);

  let templateId;
  switch (templateType) {
    case 'generate': templateId = 'generate_code'; break;
    case 'translate': templateId = 'translate_code'; break;
    case 'analyze': templateId = 'analyze_code'; break;
    case 'ask': templateId = 'ask_question'; break;
    default: templateId = '';
  }

  const requestBody = { modelId, templateId, content, temperature, topP };

  const idToken = sessionStorage.getItem('wuxia_id_token');

  if (!idToken) {
    Auth.redirectToLogin();
    return;
  }

  fetch(apiGatewayUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + idToken
    },
    body: JSON.stringify(requestBody)
  })
  .then(response => response.text())
  .then(outputText => {
	  document.getElementById('output').value = outputText;
  })
  .catch(error => {
    console.error("Error:", error);
    alert("An error occurred: " + error);
  });
}
```

- index.html: updated to add script cognito.js

```html
<body>
  ...  
  <script src="cognito.js"></script>
  <script src="wuxia.js"></script>
</body>
```

### Upload new UI files to S3

Upload the modified files to the app S3 bucket:
- cognito.js
- wuxia.js
- index.html

### Refresh your CloudFront distribution cache

Create an invalidation for:
- /cognito.js
- /wuxia.js
- /index.html
- /wuxia.css (optional)

![Alt text](../images/cognito-cloudfront-create-invalidation.png?raw=true "Invalidate CloudFront cache")

Et voilà...