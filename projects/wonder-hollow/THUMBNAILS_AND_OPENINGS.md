# Wonder Hollow thumbnail and opening handoff

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


## Upload resume after owner verification — 2026-10-11

Owner said verification was done. Reloaded counting-to-3 Studio details and reached the upload file chooser without the previous phone-verification dialog. File selection failed because the Chrome ChatGPT extension requires Details → Allow access to file URLs. No thumbnail was applied; Save remained disabled. Studio still displayed the one-off verification notice for clickable external description links, so those are not confirmed enabled. Owner was given the extension-setting handoff; the Studio tab was retained. Next: enable file access, apply/save all three prepared thumbnails, inspect Search Console sitemap/indexing, then compare subsequent CTR and retention against the recorded baseline. No new traffic gains measured.
