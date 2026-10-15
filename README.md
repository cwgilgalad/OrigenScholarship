# OrigenScholarship

Was Origen of Alexandria condemned as a heretic? This repository holds a survey of what the sources say and what scholars have argued about it, from Origen's own century to the arguments still going on today. It's written for readers of an open-access Origen reading list, and it doesn't pick a side.

The question, in the reader's words:

> Was Origen of Alexandria actually condemned as a heretic? If so, by whom, when and with what authority, and was it justified? If Origen himself was not condemned, what did others condemn instead? Was universal salvation (apokatastasis) as such condemned?

## The short version

- **c. 231.** Demetrius, Origen's own bishop, censured him in two Alexandrian synods. The grievance was mainly his ordination at Caesarea, and the churches of Palestine ignored the sentence.
- **c. 400.** A synod under Theophilus of Alexandria condemned Origen and his books, and Pope Anastasius I joined in. This was a regional act, and universal salvation wasn't the charge that carried it.
- **543.** Justinian issued an edict with ten anathemas. The ninth condemns the idea that the punishment of demons and the wicked will end in restoration, and the tenth names Origen. It's the plainest text against universal salvation anywhere in the record, but it had imperial and local authority, not a council's.
- **553.** The bishops gathered at Constantinople signed fifteen anathemas against an Origenist system. Most historians now date them to before the council formally opened, which is why they aren't in its Acts. Origen's name does appear in the council's eleventh anathema, though some scholars hold that it was added later.
- **What the 553 texts describe** is mostly a sixth-century system that specialists trace to Evagrius of Pontus and his followers, not Origen's own writings.
- **Whether universal salvation as such was condemned** is still disputed. One side reads the 543 and 553 texts as ruling it out. The other reads them as condemning a version tied to the pre-existence of souls, which leaves Gregory of Nyssa's universalism untouched. Gregory was never condemned and is venerated as a saint.

The full argument, with every position and who holds it, is in the report.

## What's here

| File | What it is |
|---|---|
| [`research/REPORT.md`](research/REPORT.md) | The survey. Origen's life and first censure, the controversy around 400, the documents of 543 and 553, whether the condemned doctrines are really Origen's, how binding the condemnations are in each tradition, whether they were just, and where the debate stands now. |
| [`research/claims.md`](research/claims.md) | Every factual claim in the report (63 of them), each with its source and how far it was checked. |
| [`research/balance-audit.md`](research/balance-audit.md) | A review of the report for bias: who gets heard, whose case is put at its strongest, and what was changed as a result. |

## How it was checked

Each claim is marked with how far it was checked:

- **V**: checked against a primary text or a scholar's own words
- **S**: checked against a reliable secondary account
- **R**: taken from standard scholarship and not yet checked against the book itself
- **C**: corrected during checking

Four claims were corrected and none turned out false. The balance audit asked whether a careful reader on each side would recognise their own case. Where the draft leaned one way, the text was changed.

## Known gaps

- Dr Cyril Jenkins is heard only through his critic, Fr Aidan Kimel: the interview itself couldn't be found. Hart is now quoted from his own essay.
- Guillaumont, Edwards and Clark are cited from secondary sources (the publisher, a reference guide, a review), not the books.
- Page references to Richard Price's translation of the 553 Acts come from other writers' citations.

## The canvas

[`canvas/`](canvas/) holds the source of the **Origen Design Showcase**, the Claude Design canvas this project began from. It presents the reading list as a responsive web page: the free English translations, what survives of the commentaries, what isn't free yet, and, since this release, a section asking **Was Origen condemned?** That section sets the condemnations out in order, with the authority each one carried, and gives both answers to the universal-salvation question with the names behind each. It links back to the report here.

- `canvas/Main.dc.html` is the page itself, as a Design Component file.
- `canvas/canvas.json` is the canvas index.

The live canvas is private to its owner on claude.ai. These files are the copy of record.

## Status

Version 1.0.0 is finished. The one limit left is Dr Jenkins, whose interview couldn't be found, so his view is given as his critic reports it. See [`CHANGELOG.md`](CHANGELOG.md) for what changed in each version.

## License

The repository carries the GNU GPL v2 (see [`LICENSE`](LICENSE)). Quotations from ancient and modern authors belong to their translators and publishers and are quoted for commentary.
