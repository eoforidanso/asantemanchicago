# AACM admin page: setup and use

The admin page lives at **https://chicagoasanteman.org/admin/**. An admin signs in with a GitHub
account, then can upload gallery photos, edit events, chiefs and queens, and change the donation
link, newsletter address and contact details. Each Save publishes to the live site in about a minute.

## One-time setup (about 20 minutes)

### 1. Make a GitHub sign-in app
1. Sign in to GitHub as the owner of the `asantemanchicago` repository.
2. Go to Settings > Developer settings > OAuth Apps > New OAuth App.
3. Application name: `AACM admin`. Homepage URL: `https://chicagoasanteman.org`.
4. Authorization callback URL: `https://YOUR-WORKER-ADDRESS/callback` (you get the address in step 2;
   come back and fill this in, or use a placeholder now and edit it after).
5. Create the app. Copy the **Client ID**, then choose "Generate a new client secret" and copy the **secret**.

### 2. Put the sign-in gateway on Cloudflare (free)
1. Sign in at dash.cloudflare.com, go to Workers & Pages > Create > Worker. Name it `aacm-admin-sign-in`.
2. Open the Worker's editor, replace its code with the contents of `tools/oauth-worker/worker.js`, and deploy.
3. Settings > Variables: add `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET` (as a Secret) and
   `SITE_ORIGIN` = `https://chicagoasanteman.org`.
4. Copy the Worker's address (it ends in `.workers.dev`). Put it into the GitHub app's callback URL
   (step 1.4) as `https://THAT-ADDRESS/callback`.

### 3. Tell the admin page where the gateway is
In `admin/config.yml`, replace `https://REPLACE-WITH-YOUR-SIGN-IN-ADDRESS` with the Worker's address
(no trailing slash), then commit and push.

### 4. Add each admin
On GitHub, open the repository > Settings > Collaborators > Add people. Each admin needs their own free
GitHub account and must accept the invitation. Only people added here can publish.

## Using it
1. Go to `/admin/` and choose "Login with GitHub".
2. Pick a section on the left: **Gallery photos**, **Events**, **Chiefs, queens and officers**, **Site settings**.
3. Make the change and press **Publish > Publish now**. The live site updates in about a minute.

Notes for admins:
- Photos: use JPG or PNG. Large photos are resized automatically. Always fill in "What the photo shows".
- Chiefs and queens: the order in the list is the order on the page. Portraits should be taller than wide.
- Every Publish goes live straight away. To undo a mistake, edit and publish again, or ask the site owner
  to restore the earlier version on GitHub (nothing is ever lost).
- The donation link and the Mailchimp address must start with `https://`. Anything else is ignored.

## How it works
- The admin page edits the files in `src/data/` and uploads photos to `assets/img/`.
- A GitHub Action (`.github/workflows/build.yml`) runs `build.py` on every change to `src/`, commits the
  rebuilt pages and asks GitHub Pages to publish.
- Page text that is not in a list (History, About and so on) is not edited here; ask the site owner.
