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

No baseline reports were read. No CTR target, traffic lift, Core Web Vitals pass or channel
public-status conclusion is established. Additional child-directed tracking needs its own
consideration; none was added in this work.

## Sources used in the original audit

- [Google AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google video SEO practices](https://developers.google.com/search/docs/appearance/video)
- [YouTube discovery/performance guidance](https://support.google.com/youtube/answer/141805?hl=en)
- [YouTube description tips](https://support.google.com/youtube/answer/12948449?hl=en)
- [YouTube Made for Kids guidance](https://support.google.com/youtube/answer/9528076?hl=en)
