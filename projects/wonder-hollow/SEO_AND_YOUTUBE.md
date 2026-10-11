# Wonder Hollow SEO, AI discovery and YouTube

Audit/release date: 2026-10-11 (Australia/Sydney).
[Project status](README.md) · [Deployment evidence](DEPLOYMENT.md)

## Baseline findings

The homepage was already static, readable HTML with social previews and GA4. It was not
a JavaScript-only shell. Its generic title/description did not clearly describe preschool
learning. Canonical URLs, sitemap, robots file and JSON-LD were absent.

Catalogue links used story titles without the ledger's learning concepts. For example,
"One Whole Hand And More" teaches counting to eight; this is weaker topic context than
"Counting to 8 Song for Preschoolers".

The publisher included an offline task but no website/channel links or explicit English
metadata. Its private upload mode is intentional. Neither an upload record nor a linked
video proves that the video is public.

An initial search query did not surface the exact domain. This does not establish an
indexing failure or index count. Search Console reports are needed to diagnose indexing.

## Implemented and deployed website changes

- Homepage title: **Preschool Learning Games & Videos (Ages 3–5) | Wonder Hollow**.
- Description: "Explore gentle preschool learning games and videos for ages 3–5.
  Practise counting, phonics, science and feelings with Wonder Hollow’s Australian animal friends."
- Matching Open Graph and Twitter title/description/image metadata; visible hero text
  names preschool games, videos, age range and learning topics.
- Canonicals on homepage, parent learning guide and privacy page.
- Connected Organization, WebSite and WebPage JSON-LD, with stable identifiers and
  the official YouTube channel in Organization.sameAs.
- Wildcard crawl allow in robots.txt and a sitemap containing the three actual page URLs.
- Parent learning guide at https://wonder-hollow.com/learning.html: counting, first sounds,
  science/nature, feelings, places/languages, shared activities, visible FAQs and creator contact.
- Learning concepts next to all 26 catalogue links, generated from the ledger so they
  survive future catalogue regeneration.
- No new analytics/tracking was added. The existing games and human approval gate remain.

## Future-upload improvements

`src/kidsvideo/publisher.py` now adds parent context (ages 3–5), watching/pausing/offline
activity guidance, and these links to upload descriptions:

- https://wonder-hollow.com/
- https://wonder-hollow.com/learning.html
- https://www.youtube.com/@WonderHollowLearning

It sets defaultLanguage and defaultAudioLanguage to English.
`src/kidsvideo/scriptwriter.py` requests accurate topic-first titles, under 100 characters
and preferably under 70, with topic and ages in the description's opening. It asks for
relevant tags without stuffing and keeps metadata instructions separate from narration rules.
Existing videos do not automatically receive these edits.

## AI discovery decisions

Google AI Overviews and AI Mode use ordinary SEO foundations: crawlability, index eligibility,
useful textual content, internal links, page experience and accurate structured identity.
No special llms.txt or AI schema is required to appear in those Google features.

Wildcard robots allow already covers compliant crawlers. Listing training-bot names is
not a ranking improvement. Training permission and search retrieval are different decisions.
The absence of llms.txt was not treated as a discovery blocker here.

Do not promise rankings, AI citations or traffic from these changes. Structured data must
match visible content. Do not add VideoObject merely because a ledger row has a video ID:
verify public playback, thumbnail and publication date first.

## Work still outstanding

| Priority | Action | Evidence required |
| --- | --- | --- |
| 1 | Submit the sitemap in the existing Search Console property | Submission/status report |
| 1 | Inspect homepage and learning guide; request indexing if appropriate | Google-selected canonical, rendered HTML, indexing exclusions and HTTP response |
| 1 | Confirm reviewed episodes are Public in YouTube Studio | Actual video visibility, not ledger IDs |
| 2 | Improve existing titles and description openings | Content review and baseline impressions/search terms |
| 2 | Review thumbnails at phone size | Existing thumbnails and channel CTR/retention data |
| 2 | Group public episodes into topic playlists | Studio or channel playlist inventory |
| 2 | Check captions and add accurate ones where missing | Published audio/caption review |
| 3 | Measure mobile page performance | PageSpeed/Core Web Vitals results |
| 3 | Create individual episode/watch pages | Public video status and reviewed transcripts/metadata |

Recommended playlists: Counting & Numbers; Letter Sounds; Preschool Science & Nature;
Feelings & Bravery; Places, Languages & Long Ago.

Dedicated watch pages should make one playable video the main content, provide a specific
title, summary, reviewed transcript and offline activity. A production script is not
automatically a verified transcript of the published audio.

## Proposed titles for existing videos

These were suggestions only, not live edits. Review against the actual videos before use:

- Counting to 8 Song for Preschoolers | Wonder Hollow
- Counting to 10 for Preschoolers | Wonder Hollow
- Letter S Sound for Preschoolers | Wonder Hollow
- Float or Sink? Preschool Science | Wonder Hollow
- Big Feelings and Deep Breaths for Preschoolers | Wonder Hollow

Keep creative story names in descriptions where useful. Match thumbnails and titles to
the real topic; avoid exaggerated learning promises. Begin with videos that already get
impressions so results can be compared. No search-volume research was completed.

## Proposed channel description

This copy was prepared for review, not applied in Studio:

> Wonder Hollow makes gentle preschool learning videos for children aged 3–5.
> Join Mossy the koala, Tilly the quokka, Rufus the kookaburra and Bimble the bilby
> to explore counting, letter sounds, science, nature and feelings — one idea at a time.
> Watch together with a grown-up, pause to answer and try an activity away from the screen.
> Explore our free learning games and parent guide at https://wonder-hollow.com/.

## Measurement plan

Save a baseline before editing the existing channel:

- **Search Console:** indexed pages, non-brand queries, impressions, clicks, CTR and position.
  Compare equivalent 28-day windows, accounting for a new/small site.
- **YouTube:** traffic sources, search terms, impressions, CTR, first-30-second retention,
  average percentage viewed and watch time. Compare similar topics and formats.
- **GA4:** organic landing pages and engagement using existing reporting.
- **AI discovery:** available referrals/citations as supporting observations, not universal
  retrieval or recommendation evidence.

A Studio baseline was read later in this session; see the dated section below. No CTR
target, traffic lift, Core Web Vitals pass or exhaustive public-status audit is established. Additional child-directed tracking needs its own
consideration; none was added in this work.

## Sources used in the original audit

- [Google AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google video SEO practices](https://developers.google.com/search/docs/appearance/video)
- [YouTube discovery/performance guidance](https://support.google.com/youtube/answer/141805?hl=en)
- [YouTube description tips](https://support.google.com/youtube/answer/12948449?hl=en)
- [YouTube Made for Kids guidance](https://support.google.com/youtube/answer/9528076?hl=en)

## Studio access and baseline confirmed 2026-10-11

Owner reported the connection working from Codex Desktop. Browser inventory now exposed
the signed-in Chrome Studio tab for Wonder Hollow; the channel dashboard, Content,
Analytics and Customisation pages were read. Earlier unavailable-browser notes are historical.
No channel metadata or visibility was changed in this follow-up. Search Console remains unread.

Reporting period: **12 September–9 October 2026 (28 days)**.
- Overview: 436 views, 3.2 watch hours, +4 subscribers; current subscriber count 7.
- Content report: 434 views (a different report scope), 12,936 thumbnail impressions,
  2.4% thumbnail CTR and 0:26 average view duration.
- Traffic sources: Suggested videos 82.5%; Browse 7.6%; Other YouTube features 4.6%;
  Channel pages 1.6%; Direct/unknown 1.4%; Others 2.3%.
- 97.9% of thumbnail impressions came from YouTube recommending the content.
- Search-query control reported insufficient data; do not claim zero search traffic.
- Four, Then Five: 196 period views, 0:27 average duration, 11.6% average viewed.
  One, Two, Three: 139 views, 0:20, 9.7%.
  One Whole Hand And More: 41 views, 0:26, 11.0%.
- Intro report (latest videos, last 365 days): 22% still watching at 0:30 for
  Four, Then Five; 19% for One, Two, Three. This is not the same window as the 28-day totals.

Channel profile description is empty (DOM value verified), with no configured external
link visible. Home tab is switched off (aria-checked=false). Layout inventory shows
Videos (26) and Created playlists (1), whose tile says 27; this does not establish
27 public videos. Content showed many older episodes Public, including Two Hands Hold
Ten Fingers, The Shadow Walk and One Whole Hand And More. Newest French Numbers Un,
Deux, Trois for Preschoolers | Wonder Hollow (X1ruZT-fDE8) is Private; keep human review.
This is a visible sample, not an exhaustive public-visibility audit.

Interpretation: YouTube already supplies impressions. Improving topic clarity and
thumbnail clicks, and especially the first 30 seconds, appears more urgent than
adding AI-specific files. Counting videos dominate observed period views; this does
not prove search demand or explain the early drop-off.

Next actions: apply the prepared parent-facing channel description and website/guide
links; enable the Home tab and organise topic playlists; pilot accurate topic-first
titles/thumbnails on the three counting videos with baseline records; review their
actual opening/audio before changing pacing. Measure comparable subsequent windows
without claiming a causal lift from this baseline.

## Channel improvements applied 2026-10-11

Owner explicitly requested "make the improvements" and "link it to the Website".
Used the connected Chrome Studio UI. Published a preschool/age/learning-topic channel
description, added profile links "Free preschool learning games" to https://wonder-hollow.com/
and "Parent guide and activities" to https://wonder-hollow.com/learning.html, and enabled
the Home tab. Studio reported Changes published / All changes saved.

Saved topic-first titles and parent-facing descriptions for:
- hJB4JJgrj8E: Four, Then Five → Counting to 5 for Preschoolers | Four, Then Five | Wonder Hollow
- EoPN3GzdScw: One, Two, Three → Counting to 3 Song for Preschoolers | One, Two, Three | Wonder Hollow
- Qvp0b5w5Otc: One Whole Hand And More → Counting to 8 Song for Preschoolers | Wonder Hollow

Read existing Studio descriptions to verify counting topics and whether each video was
a song. Preserved story context and offline activities, added ages 3–5 and parent guidance,
and included website, guide and official channel URLs. These were metadata-only edits,
not a review or change of the rendered audio. Original wording is in the Codex rollback
record projects/wonder-hollow/CHANNEL_CHANGES_2026-10-11.json.

Created a public playlist "Counting & Numbers for Preschoolers | Wonder Hollow" and
saved membership for the three already-public videos:
https://www.youtube.com/playlist?list=PLGtG87TvU0mQ
Public channel showed this playlist with 3 videos. Its description includes parent
context and website/guide links. No private video visibility or Made for Kids setting changed.

Verification: live website's YouTube link opened the correct @WonderHollowLearning channel;
public channel Home tab displayed, with the new description and homepage link. About
dialog showed both configured profile links. Public channel also displayed edited titles
and the public 3-video counting playlist. Studio showed successful saves for video edits.
Screenshots of published Studio and public channel were captured in the conversation.

Limitation: Studio displays "To make external links clickable, first complete a one-off
verification" beside video descriptions. Profile website links are published, but
clickable video-description URLs require the owner's YouTube verification. No identity,
phone or account-verification process was attempted. Thumbnails, published audio, captions,
other video metadata and Search Console were not changed in this follow-up.
No traffic or retention improvement is measured; use the prior dated baseline.

## Counting thumbnails and future openings — follow-up 2026-10-11

Owner authorised continuation with "go". [Wonder_Hollow PR #8](https://github.com/MatthieudeLaMettrie/Wonder_Hollow/pull/8) merged at `47747101d3950bf439407a40799899515388d964`. Final CI passed 193 tests; [website deployment 38101882213](https://github.com/MatthieudeLaMettrie/Wonder_Hollow/actions/runs/38101882213) succeeded.

Future scriptwriter prompts now start with the learning activity and request an early question/pause. Validation requires a pause beat in one of the first two scenes; a regression test rejects openings whose pauses occur only later. This does not change published audio or guarantee a measured retention improvement.

A deterministic Pillow renderer composites unchanged locked character PNGs into three 1280×720 JPEG thumbnails, each below 2 MB. No character regeneration or paid episode production was triggered. Assets are committed under `packs/seo-thumbnail-pilot/` and `website/assets/thumbnails/`. All three live images were visually reviewed for wording, quantity dots and layout:

| Existing public video | Prepared thumbnail |
| --- | --- |
| EoPN3GzdScw — counting to 3 | https://wonder-hollow.com/assets/thumbnails/EoPN3GzdScw.jpg |
| hJB4JJgrj8E — counting to 5 | https://wonder-hollow.com/assets/thumbnails/hJB4JJgrj8E.jpg |
| Qvp0b5w5Otc — counting to 8 | https://wonder-hollow.com/assets/thumbnails/Qvp0b5w5Otc.jpg |

**No thumbnail was applied in YouTube.** Studio's upload attempt opened "Unlock more on YouTube": "To add custom thumbnails, verify your phone number." Owner phone verification is also required for clickable external video-description links. A Studio tab with the Verify dialog was left for the owner. The owner must complete verification directly; do not request phone numbers or codes in chat.

Resume after owner confirms verification: recheck Studio eligibility, upload the corresponding JPEG to each existing public video's Thumbnail / Upload file control, save and verify each result. Preserve visibility and Made for Kids settings. One local download (counting-to-3) succeeded; subsequent browser download attempts timed out/reset the browser runtime, so local availability of the other files is unconfirmed. Hosted URLs above remain usable.

Channel profile links, playlist and metadata improvements from the earlier follow-up remain applied. Search Console has not been inspected. No traffic, CTR, ranking or retention gains have been measured. Keep baseline windows comparable when checking results.


## Search Console verified, sitemap submitted and homepage recrawl requested — 2026-10-11

After owner's completion, refreshed Search Console and found the https://wonder-hollow.com/ URL-prefix property in the confirmed account. Overview reports are processing; no performance totals available yet. Submitted sitemap.xml: Google confirmed Sitemap submitted successfully, but the row showed Unknown / Couldn't fetch / 0 discovered pages and videos. Details say Sitemap could not be read. Submission acceptance is not successful ingestion or indexing.

Investigated: browser sitemap navigation returned ERR_BLOCKED_BY_CLIENT; web tool could not fetch sitemap/robots; local curl could not start because of the existing exec helper failure. Re-ran the existing website deployment job 114359323942 (run 38101882213, attempt 2). Replacement job 114375162315 succeeded, redeployed the website and exact live-file checks passed, including sitemap.xml on custom and Firebase domains plus real 404s. This verifies hosting from the runner; it does not establish why Google's initial fetch failed. Retried sitemap once after that successful check; submission accepted again. Fetch/ingestion success remains outstanding; recheck later, avoid repeated submissions without new evidence.

Homepage URL Inspection: Google's 5 October 2026 crawl had no user canonical and selected https://www.wonder-hollow.com/; current https://wonder-hollow.com/ URL was not indexed (Duplicate without user-selected canonical). That historical crawl predates the 11 October canonical changes. Live test on 11 October at 14:05 showed URL is available to Google, successful smartphone fetch, crawl/indexing allowed, and user-declared canonical https://wonder-hollow.com/. Requested indexing; Google confirmed Indexing requested and priority crawl queue placement. Index inclusion/canonical selection is not yet proved.

Count-to-8 Qvp0b5w5Otc still has original auto-generated thumbnail in Studio. Owner asked where the new image is; supplied https://wonder-hollow.com/assets/thumbnails/Qvp0b5w5Otc.jpg and Save image as → Downloads → Qvp0b5w5Otc.jpg instructions. Await confirmed local save to upload it. Count-to-3/5 custom thumbnails remain applied. Preserved Studio/image handoff and Search Console result tabs. No visibility change, new paid episode or traffic uplift claimed.
