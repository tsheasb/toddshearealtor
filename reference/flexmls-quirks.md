# FLEX MLS — Known Quirks

Reference for pulling market stats and listing data via the FLEX MLS MCP
connector.

## Listing search

- `ListingsListingSearch` requires both `status_values` and
  `property_type_codes` arrays passed explicitly, even when you want to
  search across all statuses/types. Don't omit them expecting a sane
  default — the call needs the full arrays every time.
- Filter syntax: `_filter="ListingId Eq '26-XXXX'"`
- Always include in `_select`: `ListingId, UnparsedAddress, ListPrice,
  MlsStatus, BedsTotal, BathsTotal, BuildingAreaTotal,
  ListAgentFirstName, ListAgentLastName, ListOfficeName, City`
- Use `ListAgentFirstName` + `ListAgentLastName` — NOT `ListAgentFullName`,
  which returns nothing.
- Team names sometimes populate the agent name field directly (e.g.
  "Marsha Kotlyar Estate Group" instead of a first/last name). This is an
  MLS data-entry pattern, not a tool error — use it as-is in attribution,
  don't try to "fix" it into a fake first/last split.

## Market statistics

Price, days on market, and inventory require **separate tool calls** —
there's no single combined stats endpoint.

Location parameters:
- Montecito: `LocationField: City`, `LocationValue: MONTECITO`,
  `PropertyTypeCode: A` for single-family homes
- Santa Barbara: `LocationField: City`, `LocationValue: SANTA BARBARA`
  (all caps required)
- Same all-caps City pattern applies to other SB County cities/areas.

Small-sample markets (Montecito in particular, ~10 sales/month) swing hard
month to month on median price. Always pull at least the current month plus
one prior month and one year-ago month for comparison, and note the caveat
in copy rather than presenting a single median as a clean trend.

## Listing photos

`ListingsListPhotos` returns photo URLs on `sparkplatform.com` (or
`cdn.resize.sparkplatform.com`). These are **hotlink-blocked by Mailchimp**
— they render fine on the live web page but break in the email send. See
`workflow.md` for the required re-hosting step before every send.

Double check the exact photo ID/URL copied into a post — a single-digit
typo in a photo ID (e.g., transposed numbers) will silently fail or return
a tiny redirect/placeholder image instead of erroring loudly. Verify file
size or dimensions after downloading, don't assume a 200 response means the
right image came through.
