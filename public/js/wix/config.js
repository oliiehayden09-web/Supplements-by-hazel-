// Hazel's public Wix OAuth client id (not a secret: it only mints anonymous visitor tokens).
// Set when the site is deployed through Wix "Go Headless" (the migration's WIX_CLIENT_ID).
// Until then the shop can't load: never paste Perform's id here, or the pages read Perform's store.
export const WIX_CLIENT_ID = "SET-ON-DEPLOY";
