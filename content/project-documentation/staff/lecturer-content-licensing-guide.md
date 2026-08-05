# Practical Licensing Guide For Lecturers

This guide is for BiGHT lecturers preparing course website pages, Markdown content, exercises, or slides for public release on GitHub or the public course website.

It is practical guidance, not legal advice. If a case is genuinely uncertain, ask the relevant EPFL support channel before publishing. The EPFL Library maintains a "Citation and copyright" page with a teaching-activities section and a copyright-team contact route: https://www.epfl.ch/campus/library/training/citation-copyright/.

## Core Rule

You may license under CC BY 4.0 only material for which you have the necessary rights.

Usually safe to license under CC BY 4.0:

- Your own original text, diagrams, exercises, and slides.
- Original material co-authored with colleagues who have agreed to release it under CC BY 4.0.
- Material where a contract, permission, or existing license allows sublicensing or republication under CC BY 4.0.

EPFL Library guidance states that instructors retain copyright in course materials they created, and that CC licensing requires consent of co-authors and authorizations for third-party material reuse. Apply that principle to each item rather than assuming rights for the whole deck.

Not safe to license under CC BY 4.0 without checking:

- Publisher figures.
- Journal or book excerpts.
- Screenshots.
- Stock photos, icons, maps, videos, fonts, and templates.
- Material from guest lecturers, students, partner organisations, or previous course editions.
- AI-generated assets if the service terms, prompt inputs, or source material create uncertainty.

## Class Presentation Vs Public Redistribution

Showing an item during a live class and redistributing the slides publicly are different acts.

For class teaching, certain uses may be permitted by institutional subscriptions, classroom rules, quotation rights, or statutory exceptions. For public GitHub or website release, you are distributing a copy to the public. That usually requires either your own rights, an open license, permission, public-domain status, or a clearly applicable legal exception.

Do not assume that material shown in class can also be published in public slides.

## Co-Authored Slides And Contributions

Before publishing co-authored material under CC BY 4.0, confirm that the authors agree to that license for their contributions.

Handle contributors as follows:

- Colleagues: credit their contributions and confirm permission for CC BY 4.0 release.
- Guest lecturers: do not publish their slides under the course license unless they agree.
- Students: do not publish student work under the course license unless the student has granted the required rights.
- Partner organisations: do not assume organisational material is reusable; ask for written permission or use a public version they provide.
- Previous course editions: check authorship and third-party content again before republishing.

Do not imply that one contributor owns or licenses the whole collection.

## Creative Commons Material

When using CC-licensed material, check:

- Creator.
- Title, when available.
- Source link.
- Exact license and version.
- Whether adaptations are allowed.
- Whether commercial use is allowed.
- Whether ShareAlike applies.
- Whether you modified the material.

Creative Commons recommends clear marking of author, license, and machine-readable information where possible. See:

- CC BY 4.0 deed: https://creativecommons.org/licenses/by/4.0/
- CC BY 4.0 legal code: https://creativecommons.org/licenses/by/4.0/legalcode.en
- Creative Commons marking guidance: https://wiki.creativecommons.org/wiki/Marking/Creators
- Creative Commons license overview: https://creativecommons.org/share-your-work/cclicenses/

### Attribution Format

Use this pattern:

> [Title] by [creator], [source link], licensed under [license name/version] ([license link]). [Changes made, if any].

Example:

> "Ebola virus virion" by [creator], [source URL], licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Cropped.

If no title is available:

> Map of affected provinces by [creator], [source URL], licensed under CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/). Labels added.

## Compatibility Issues

CC BY material can generally be incorporated into a CC BY deck if you provide attribution and mark changes.

CC BY-SA material requires care. If you adapt CC BY-SA material, the adaptation usually must be shared under the same or a compatible ShareAlike license. Do not present a slide deck as if the whole adaptation is CC BY if it contains adapted CC BY-SA material that triggers ShareAlike obligations. Instead, keep the CC BY-SA item clearly marked, avoid adapting it when possible, or ask for advice.

CC BY-NC, CC BY-ND, and CC BY-NC-ND are often problematic for public course repositories. NonCommercial, NoDerivatives, and other restrictions may conflict with reuse goals or planned modifications.

## Third-Party Items To Check Carefully

Attribution alone is not permission. Check the actual terms for:

- Publisher figures and tables.
- Screenshots of software, websites, dashboards, and interfaces.
- Stock-photo and stock-icon libraries.
- Map tiles and geospatial data providers.
- Icon libraries and font licenses.
- Videos and audio clips.
- AI-generation services and generated images.
- Datasets and database extracts.
- Logos and trademarks.

Some resources allow classroom display but not public redistribution. Some allow use only with attribution. Some prohibit modification. Some require a paid plan or separate permission for redistribution.

## Label Excluded Third-Party Items On The Slide

Every third-party item should be marked directly on the relevant slide or in a clearly linked credits slide. The label should make clear that the item is not covered by the deck's CC BY 4.0 license unless that is actually true.

Use:

> [Item] by [creator], from [source]. [License/permission/legal basis]. Not covered by this deck's CC BY 4.0 license.

For copyrighted material reproduced with permission:

> [Item] by [creator], from [source]. Reproduced with permission of [rights holder], [year]. Not covered by this deck's CC BY 4.0 license.

For material used under an exception:

> [Item] by [creator], from [source]. Used here under [identified exception, if known]. Not covered by this deck's CC BY 4.0 license.

If the exception is not clear, do not guess. Escalate or replace the item.

## If Rights Are Unclear

Use one of these options:

- Replace the item with your own original figure.
- Use a clearly licensed alternative.
- Obtain written permission for public redistribution.
- Link to the original instead of reproducing it.
- Keep it only in the private classroom version.
- Make a separate public version of the slide without the item.

Do not publish a public deck containing items marked only as "source: Google Images", "from paper", "Pinterest", "unknown", or similar.

## Public Deck Notice

Put this on a title slide, final slide, or credits slide:

> Except where otherwise indicated, original content in this presentation is © [year] [author(s)] and licensed under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. Third-party materials are excluded from this license and remain subject to their indicated rights.

Use "except where otherwise indicated" only if the exceptions are actually and visibly indicated.

## Pre-Publication Checklist

Before publishing slides or Markdown content:

- Confirm that original content authors agree to CC BY 4.0 release.
- Remove private speaker notes and internal drafting comments.
- Check every image, figure, screenshot, map, icon, font, dataset, quotation, and video.
- Add point-of-use attribution for every third-party item.
- Mark material reproduced with permission as permission-based, not CC BY.
- Mark material used under an exception as excluded from CC BY.
- Remove or replace items with unclear rights.
- Check CC BY-SA, NC, and ND terms before incorporating CC material.
- Preserve license and attribution notices from adapted materials.
- Verify that no logo, trademark, or visual identity is implied to be CC-licensed.
- Include the deck-level notice from `SLIDE-LICENSING-NOTICES.md`.
- Keep a private record of permissions where relevant.

## Preserve Attribution When Adapting

When adapting someone else's content, preserve the creator, title if available, source, license, and modification history. CC BY 4.0 requires attribution and indication of changes when sharing modified material.

Recommended modification notes:

- "Cropped."
- "Translated from French."
- "Colors changed and labels added."
- "Excerpted from original."
- "No changes made."

## Swiss Copyright Sources

For Swiss copyright background, use official sources rather than informal summaries:

- EPFL Library, Citation and copyright: https://www.epfl.ch/campus/library/training/citation-copyright/
- Swiss Federal Institute of Intellectual Property copyright overview: https://www.ige.ch/en/protecting-your-ip/copyright
- Federal Act on Copyright and Related Rights on Fedlex: https://www.fedlex.admin.ch/eli/cc/1993/1798_1798_1798/en

This guide does not interpret Swiss copyright exceptions for a specific slide or public release. If your use depends on an exception or limitation, get advice before publishing.
