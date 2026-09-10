---
layout: week
title: "Week 4: Reshaping and Joining Relational Tables"
week_number: 4
---

# Two Tables, One Household

## A Family, Split Across Files

Every dataset you've worked with so far this semester has lived in exactly one file. Real organizations almost never get that luxury. A hospital doesn't keep one table with every fact about a patient — it keeps a table of visits, a table of prescriptions, a table of billing codes, each maintained by a different department, updated on a different schedule, sometimes by a different piece of software entirely. Understanding data at that scale means understanding how separate tables relate to each other, not just what's inside any one of them.

This week's dataset is smaller, but it's built to behave the same way: **two tables about the same four-person household**, kept separately, the way a wearable fitness tracker and a clinic's own records actually would be.

**📥 Download the datasets: [health_monitoring.csv](https://cs.calvin.edu/courses/data/202/26fa/datasets/health_monitoring.csv) and [family_profiles.csv](https://cs.calvin.edu/courses/data/202/26fa/datasets/family_profiles.csv)**

This is a teaching dataset, built to behave like real household health records — one table logging daily vitals and meals (as a wearable device or health app might export them), and a second, much smaller table of family-member profiles (as a clinic's intake system might keep them). Treat the *shapes* of the patterns as realistic and the *exact numbers* as illustrative. Download both files now; every table and number below comes from running the code shown directly on them.

```python
import pandas as pd

monitoring = pd.read_csv("health_monitoring.csv")
profiles = pd.read_csv("family_profiles.csv")

monitoring.head(3)
```

| Name | Date | Heart Rate (bpm) | Blood Pressure (mmHg) | Steps | Sleep Duration (hours) | Food Morning | Food Afternoon | Food Evening |
|:---|:---|---:|:---|---:|---:|:---|:---|:---|
| Alice Johnson | 2024-01-14 | 87 | 125/74 | 12,302 | 6.2 | muffin, smoothie, yogurt | tofu stir-fry, soda, green tea | mashed potatoes, green beans, steak |
| David Johnson | 2024-07-13 | 62 | 122/87 | 12,548 | 8.8 | cereal, muffin, orange juice | grilled chicken, burger, water | chicken curry, garlic bread, mashed potatoes |
| Bob Johnson | 2024-04-27 | 71 | 116/90 | 14,910 | 6.4 | smoothie, banana, yogurt | salad, apple, rice | chicken curry, salmon, sweet potatoes |

```python
profiles
```

| Name | Role | Birth_Year | Primary_Clinic | Has_Wearable_Tracker |
|:---|:---|---:|:---|:---|
| Alice Johnson | Parent | 1986 | Downtown Family Clinic | Yes |
| Carol Johnson | Parent | 1988 | Downtown Family Clinic | Yes |
| David Johnson | Child | 2011 | Eastside Pediatrics | Yes |
| Bobby Johnson | Child | 2013 | Eastside Pediatrics | Yes |
| Eleanor Johnson | Grandparent | 1958 | Lakeside Senior Health | No |

`monitoring` has **150 rows** — one per person, per day. `profiles` has **5 rows** — one per person, full stop. Already, two things should catch your eye: there are five names in `profiles` but only four in `monitoring`, and one of those names — `"Bobby Johnson"` versus `"Bob Johnson"` — doesn't quite match its counterpart. Keep both of those in mind. This reading is built around exactly what happens when you try to bring these two tables together.

---

# Wide and Long: What Counts as One Row

## The Shape monitoring Is In Right Now

`monitoring` is in **wide** format: every fact about one person, on one day, sits in a single row, spread across columns — including three separate meal columns, `Food Morning`, `Food Afternoon`, and `Food Evening`. That's a natural way to *enter* data (one form, one row, one submission), but it's an awkward way to *analyze* meals as their own subject. If you wanted to ask "what did this family eat most often, across all meals?", you'd have to search three columns at once.

**Melting** reshapes a wide table into **long** format: instead of three meal columns, you get one column naming *which* meal it was, and one column holding *what* was eaten.

```python
long = pd.melt(
    monitoring,
    id_vars=["Name", "Date", "Heart Rate (bpm)", "Blood Pressure (mmHg)",
             "Steps", "Sleep Duration (hours)", "Health Notes"],
    value_vars=["Food Morning", "Food Afternoon", "Food Evening"],
    var_name="Meal",
    value_name="Food",
)
long["Meal"] = long["Meal"].str.replace("Food ", "", regex=False)
long.shape
```

```text
(450, 9)
```

`id_vars` lists the columns that stay put — they get repeated on every new row. `value_vars` lists the columns being unstacked — their *names* become the values of the new `Meal` column, and their *cell contents* become the values of the new `Food` column. 150 rows × 3 meal columns becomes **450 rows × 1 meal column**, exactly the columns-into-rows trade you'd expect.

| Name | Date | Meal | Food |
|:---|:---|:---|:---|
| Alice Johnson | 2024-01-06 | Morning | toast, banana, yogurt |
| Alice Johnson | 2024-01-06 | Afternoon | fries, green tea, apple |
| Alice Johnson | 2024-01-06 | Evening | red wine, steak, green beans |

## Going Back the Other Way

**Pivoting** is melting's mirror image: long format back to wide. If you handed someone the 450-row `long` table and they wanted one row per person-day again, `.pivot_table()` gets them there:

```python
back_to_wide = long.pivot_table(
    index=["Name", "Date", "Heart Rate (bpm)", "Blood Pressure (mmHg)",
           "Steps", "Sleep Duration (hours)", "Health Notes"],
    columns="Meal",
    values="Food",
    aggfunc="first",
).reset_index()
back_to_wide.shape
```

```text
(150, 10)
```

Exactly the shape we started with. `index` lists the columns that identify a row; `columns` names the column whose *values* should become new column headers; `values` says which column supplies the contents; `aggfunc` tells pandas what to do if more than one row ever shared the same index (here, just take the first — there's never more than one match). Melting and pivoting are inverses of each other precisely because no information was thrown away in between — only rearranged.

## One More Reshape: Exploding a List Into Rows

Each `Food` cell is really *several* foods jammed into one string (`"toast, banana, yogurt"`). `.explode()` takes a column of lists and gives each list item its own row:

```python
long["Food_List"] = long["Food"].str.split(", ")
exploded = long.explode("Food_List").reset_index(drop=True)
exploded.shape
```

```text
(1350, 10)
```

450 meal-rows, each holding exactly 3 food items, becomes 1,350 single-food rows — the same columns-into-rows logic as melting, just applied to a list inside a cell instead of a set of columns. Now a question like "how often does this family eat bananas?" is a single filter:

```python
exploded[exploded["Food_List"] == "banana"]["Name"].value_counts()
```

```text
Name
Bob Johnson       13
Alice Johnson     13
David Johnson      8
Carol Johnson      7
Name: count, dtype: int64
```

Forty-one banana-eating events, across the whole family — a question the original wide table couldn't answer without first reading every one of its three food columns by hand.

## What a Reshape Doesn't Fix

Here's the catch. `monitoring` has 150 rows, but they aren't evenly split: **Alice Johnson makes up 29.3% of them** (44 rows), while David Johnson makes up only 21.3% (32 rows) — probably because Alice simply used her tracker more consistently. What happens to that imbalance once we melt to 450 rows, and again once we explode to 1,350?

```python
(monitoring["Name"].value_counts(normalize=True) * 100).round(1)
(exploded["Name"].value_counts(normalize=True) * 100).round(1)
```

```text
Name              wide %    exploded %
Alice Johnson       29.3          29.3
Carol Johnson       25.3          25.3
Bob Johnson         24.0          24.0
David Johnson       21.3          21.3
```

Identical, to one decimal place. Melting and exploding both multiply *every* person's row count by the same factor (×3, then ×3 again), so they don't distort who's over- or under-represented — but they don't fix it either. Any average computed from the long or exploded table is still quietly weighted toward whoever wore their tracker most often. **A reshape changes what a row means. It does not change whose experience the table was already better or worse at capturing.**

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**In `pd.melt(monitoring, id_vars=[...], value_vars=["Food Morning", "Food Afternoon", "Food Evening"], var_name="Meal", value_name="Food")`, what do `value_vars` specify?**

- [ ] The columns that stay the same on every row of the new long table.
- [x] The columns whose *names* become values in the new `Meal` column, and whose cell contents become values in the new `Food` column.
- [ ] The exact number of rows the long table will have.
- [ ] The columns to drop from the dataset entirely.

<!-- END QUESTION -->

---

<!-- QUESTION:fill-in-the-blank -->

The wide `monitoring` table has 150 rows and 3 meal columns. After melting those 3 columns into one `Meal`/`Food` pair, the long table has **[450]** rows, because each of the 150 person-days becomes **[3]** separate rows — one per meal.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Alice Johnson makes up 29.3% of the 150 wide rows. After melting to long format (450 rows) and then exploding individual food items (1,350 rows), what happens to her share of the table?**

- [x] It stays exactly the same, 29.3% — melting and exploding both multiply every person's rows by the same factor, so relative representation doesn't change from the reshape itself.
- [ ] It grows, because melting and exploding always amplify whoever already appears most often.
- [ ] It shrinks, because exploding splits her rows more than anyone else's.
- [ ] It's impossible to know without re-running the code.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: true
-->

Melting the three Food columns into a Meal/Food pair, and then pivoting the result back with `.pivot_table()`, returns a table with the same shape (150 rows × 10 columns) as the original wide `monitoring` table.

<!-- END QUESTION -->

# When One Table Isn't Enough: Keys and Relational Structure

## What Makes Two Tables "Related"

`monitoring` and `profiles` aren't the same table split in half — they're about entirely different *grains*. One row in `monitoring` is a person on a day; one row in `profiles` is a person, period. They have wildly different row counts (150 versus 5) and almost no columns in common. What makes them **relational** — able to be connected at all — is that they share one column whose values are supposed to mean the same thing in both places: `Name`.

That shared column is called a **key**. In a more industrial dataset you'd usually see a dedicated ID column instead of a name (a `Material_ID`, a `patient_id`, a `SKU`) precisely because names are fragile — but the underlying idea is identical: a key is a column (or set of columns) you can use to look up "which row in the other table is this row talking about?"

**Two important facts about keys, both visible right here:**

1. **Tables don't need matching row counts to be related.** `profiles` has 5 rows, `monitoring` has 150 — that's completely normal for a *one-to-many* relationship: one profile, many monitoring days.
2. **A key only works if the values actually match, character for character.** Look again at the two tables: `monitoring` has `"Bob Johnson"`. `profiles` has `"Bobby Johnson"`. To a human reading both tables side by side, these are obviously the same ten-year-old. To pandas, matching on `Name`, they are two completely different strings — no more related than `"Bob Johnson"` and `"Eleanor Johnson"` are.

This is the same string-matching logic from Week 3's cleaning work, showing up in a new and higher-stakes place. Cleaning a *category* column that's spelled inconsistently mostly costs you a slightly wrong count. Cleaning a **key** column that's spelled inconsistently costs you entire rows disappearing from a join without any error message at all — which is exactly what the next section will show you happening.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**What connects the 150-row `monitoring` table to the 5-row `profiles` table?**

- [x] A shared `Name` column — the same value has to appear in both tables for a join to find a match.
- [ ] Both tables need to have the exact same number of rows to be related.
- [ ] Nothing formal — since both tables describe the same family, pandas connects them automatically.
- [ ] The `Date` column, since both tables were collected in 2024.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: true
-->

A relational key does not require the connected tables to have the same number of rows — `monitoring` has 150 rows and `profiles` has 5, and they can still be joined on `Name`.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**`monitoring` lists `"Bob Johnson"`; `profiles` lists `"Bobby Johnson"` for the same person. What will pandas do with this, by default, when you join the two tables on `Name`?**

- [x] Treat them as two different values, since a join matches on exact string equality — `"Bob Johnson"` and `"Bobby Johnson"` are not the same string.
- [ ] Recognize they refer to the same person and merge their rows together automatically.
- [ ] Raise an error and refuse to run the merge.
- [ ] Automatically correct `"Bobby"` to `"Bob"`, since it's a common nickname.

<!-- END QUESTION -->

# Joining Tables

## Four Ways to Combine Two Tables

`pd.merge()` combines two DataFrames on a shared key, and the `how=` argument decides what happens to rows that *don't* find a match on the other side:

| `how=` | Keeps | Unmatched rows |
|:---|:---|:---|
| `"inner"` | only rows with a match in **both** tables | dropped entirely, from both sides |
| `"left"` | every row from the **left** table | right-side columns filled with `NaN` if unmatched |
| `"right"` | every row from the **right** table | left-side columns filled with `NaN` if unmatched |
| `"outer"` | every row from **either** table | `NaN` fills in on whichever side lacks a match |

None of these is simply "the correct one." `inner` is right when you only want complete, fully-matched records for an analysis. `left` or `right` is right when one table is your primary subject and you don't want to silently lose its rows just because a companion table doesn't have a match. `outer` is right when your first goal is diagnostic — surfacing *every* mismatch so you can go investigate it, which is exactly how we're about to use it.

## Running All Four, on the Same Two Tables

```python
inner = pd.merge(monitoring, profiles, on="Name", how="inner")
left  = pd.merge(monitoring, profiles, on="Name", how="left")
right = pd.merge(monitoring, profiles, on="Name", how="right")
outer = pd.merge(monitoring, profiles, on="Name", how="outer")

for name, df in [("inner", inner), ("left", left), ("right", right), ("outer", outer)]:
    print(name, df.shape)
```

```text
inner (114, 14)
left  (150, 14)
right (116, 14)
outer (152, 14)
```

Four different row counts, from the exact same two tables. Here's why each one lands where it does:

- **inner = 114**: Alice, Carol, and David's rows all match cleanly (44 + 38 + 32 = 114). Bob's 36 rows have no match (`"Bob Johnson"` ≠ `"Bobby Johnson"`) and Eleanor has no monitoring rows at all — both are dropped.
- **left = 150**: every monitoring row survives, matched or not. Bob's 36 rows are still here — just with `NaN` in `Role`, `Primary_Clinic`, and `Has_Wearable_Tracker`, because nothing on the profiles side matched.
- **right = 116**: every profile row survives. The 114 matched rows, plus one row each for `"Bobby Johnson"` and `"Eleanor Johnson"` — both appear once, with every monitoring column (`Heart Rate (bpm)`, `Steps`, ...) set to `NaN`.
- **outer = 152**: everything from both sides — the 114 matched rows, Bob's 36 unmatched rows, and the 2 unmatched profile rows (Bobby, Eleanor). 114 + 36 + 2 = 152.

```python
left[left["Role"].isnull()]["Name"].unique()
```
```text
array(['Bob Johnson'], dtype=object)
```

## Why This Isn't Just a Row-Counting Exercise

Here's what a mismatched key actually costs you in an analysis, not just in a row total. Suppose you naively left-join and then ask: what's the average heart rate at each clinic?

```python
left.groupby("Primary_Clinic")["Heart Rate (bpm)"].mean().round(1)
```

```text
Primary_Clinic
Downtown Family Clinic    79.9
Eastside Pediatrics       78.8
```

Eastside Pediatrics comes out to 78.8 bpm. But `.groupby()` silently drops rows with a missing group key — and Bob's 36 rows have exactly that: a `NaN` `Primary_Clinic`, because his name never matched. **This average was only ever computed from David's 32 rows.** Bob's entire contribution to "Eastside Pediatrics" vanished, with no warning, no error, nothing in the output to tell you it happened.

Now fix the mismatch — one line, the same kind of `.replace()` lookup from Week 3 — and rejoin:

```python
profiles_fixed = profiles.copy()
profiles_fixed["Name"] = profiles_fixed["Name"].replace({"Bobby Johnson": "Bob Johnson"})

left_fixed = pd.merge(monitoring, profiles_fixed, on="Name", how="left")
left_fixed.groupby("Primary_Clinic")["Heart Rate (bpm)"].mean().round(1)
```

```text
Primary_Clinic
Downtown Family Clinic    79.9
Eastside Pediatrics       80.7
```

Eastside Pediatrics's row count nearly doubles — 32 rows to 68 — and its average heart rate shifts by almost two full beats per minute, from 78.8 to 80.7. **Nothing about anyone's actual heart rate changed.** The only thing that changed was whether the join could find Bob at all. A join failure and a real underlying pattern can produce numbers that look equally confident and equally clean — the summary statistic itself carries no flag telling you which one you're looking at.

---

## Check Your Understanding

<!-- QUESTION:fill-in-the-blank -->

`pd.merge(monitoring, profiles, on="Name", how=...)` produces different row counts depending on the join type: `"inner"` keeps only matched rows, **[114]**. `"left"` keeps every monitoring row regardless of match, **[150]**. `"right"` keeps every profile row regardless of match, **[116]**. `"outer"` keeps everything from both sides, **[152]**.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Under the left join, Bob Johnson's 36 rows end up with `NaN` in `Role`, `Primary_Clinic`, and `Has_Wearable_Tracker`. Why?**

- [x] A left join keeps every row from the left (`monitoring`) table regardless of whether it matches; since `"Bob Johnson"` never matches `"Bobby Johnson"` in `profiles`, those columns have nothing to fill in.
- [ ] Bob Johnson's monitoring data was itself incomplete for those columns.
- [ ] pandas ran out of rows in the `profiles` table before reaching Bob.
- [ ] Left joins always leave the most recently added person's columns blank.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**A naive left join gives Eastside Pediatrics an average heart rate of 78.8 bpm from 32 rows. After fixing the `"Bobby Johnson"` → `"Bob Johnson"` mismatch and rejoining, Eastside's average shifts to 80.7 bpm from 68 rows. What actually happened?**

- [x] The first average only reflected David's 32 rows; Bob's 36 rows had a `NaN` clinic and were silently excluded by `.groupby()`, so the true Eastside average was hidden behind a spelling mismatch the whole time.
- [ ] Fixing the mismatch changed the actual heart-rate readings recorded for Eastside Pediatrics patients.
- [ ] The second `.groupby()` included rows that don't really belong to Eastside Pediatrics.
- [ ] `.groupby()` always drops whichever clinic has the fewest matched rows.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: true
-->

If every row in the left table has at least one match in the right table, an inner join and a left join on the same two tables produce the exact same set of rows.

<!-- END QUESTION -->

# Data Journeys: Following the Data Beyond the Merge

## Where the Mismatch Actually Came From

Step back and ask a question this reading hasn't asked yet: *why* does `monitoring` say `"Bob Johnson"` while `profiles` says `"Bobby Johnson"`? Nothing in the CSV files tells you directly — but the shape of the mismatch tells a story. `monitoring` reads like an export from a wearable device or health app, tied to whatever name someone typed once when they set up the account. `profiles` reads like a clinic's own intake system, filled out by a different person, on a different form, at a different time — maybe a receptionist using the name on an insurance card. Two systems, two people, two moments of data entry, and no shared ID number connecting them at the source. The mismatch isn't a bug in pandas. It's a fossil of the data's actual journey before it ever reached you as a CSV.

This is precisely the idea behind what historian and philosopher of science **Sabina Leonelli** calls a **data journey** — the path a piece of data travels through different hands, purposes, and institutions between the moment it's collected and the moment someone downstream tries to use it (Leonelli, S. (Ed.). (2020). *Data Journeys in the Sciences*. Springer International Publishing. https://doi.org/10.1007/978-3-030-37177-7). Her framework asks a consistent set of questions about any dataset, no matter the field:

- **Who collected it, and why?** What practices, institutions, and goals shaped the collection?
- **How was it prepared, cleaned, and transformed** on its way to you — and what got left out in the process?
- **How is it maintained?** What keeps it usable, correct, and available over time?
- **Who has access to it**, and who doesn't?

None of these questions has a single right answer for our two tables — but sitting with them changes how you read the numbers above.

## Two Kinds of Disappearing

This reading has now shown you two different family members vanish from an analysis, for two different reasons, and it's worth being precise about the difference:

**Bob Johnson** has real data — 36 real days of heart rate, steps, sleep, meals — sitting in `monitoring` the whole time. A careless inner join drops him anyway, purely because of a naming mismatch introduced somewhere upstream in his data's journey. Fix the key, and his data comes right back.

**Eleanor Johnson** has no monitoring data to recover, under any join. She "declined to wear the tracker" — meaning her absence isn't a cleaning problem at all, it's a genuine gap in what was ever collected about her in the first place. No amount of `.replace()` brings back data that was never gathered.

From inside a single `.merge()` call, these two situations can look identical: a name with `NaN` where health columns should be. **Knowing the difference between "the data exists somewhere, under a different key" and "the data was never collected" is not something any join operation can tell you.** It requires knowing the data's journey — which is exactly what a bare CSV file, on its own, never tells you.

## Questions Worth Asking About Any Two Tables You Join

- If you only ever inner-join, whose rows are you quietly discarding — and can you tell the difference between a spelling mismatch and a real absence?
- Who decided which column would serve as the key, and how much trust does that decision assume about two different systems spelling the same thing the same way?
- Who maintains `family_profiles.csv` going forward? If Eleanor gets a tracker next year, whose job is it to update this table, and how would you know it happened?
- If this were real household health data instead of a teaching dataset, who should be allowed to see the *joined* table — which reveals more about a person than either source table did on its own?

Reshaping and joining feel like purely mechanical operations — reorganize some rows, match some keys, done. This section has tried to show you they're not just mechanical. Every join is a claim that two records, collected by different people for different reasons, are actually about the same thing. Taking that claim seriously — checking it, not just running it — is part of the work, not a detour from it.

---

## Check Your Understanding

<!-- QUESTION:multiple-choice -->

**`monitoring` likely came from a wearable device's export; `profiles` likely came from a clinic intake form typed by a different person. What does this explain about the "Bob" vs. "Bobby" mismatch?**

- [x] Different systems, filled in by different people, have no shared ID to guarantee the same spelling of a name — exactly the kind of gap a data journey's collection stage can introduce.
- [ ] Nothing — the mismatch is a random coincidence unrelated to how the data was collected.
- [ ] It proves the wearable device company deliberately falsified its records.
- [ ] It shows that pandas cannot handle data that came from two different sources.

<!-- END QUESTION -->

---

<!-- QUESTION:true-false
answer: true
-->

When an inner join silently drops Bob Johnson's 36 rows because of a spelling mismatch, the result looks identical to a dataset where those 36 days were genuinely never recorded — even though the data exists, just under a different spelling.

<!-- END QUESTION -->

---

<!-- QUESTION:multiple-choice -->

**Eleanor Johnson appears in `profiles` but never in `monitoring`, because she declined to wear the tracker. In a report built only from an inner join of the two tables, what happens to her?**

- [x] She disappears entirely — an inner join keeps only matched rows, and she has no monitoring rows to match against.
- [ ] She appears with a heart rate of 0.
- [ ] She appears once, with every health column marked `NaN`.
- [ ] Nothing — which join type you choose has no effect on whether her row appears.

<!-- END QUESTION -->

---

<!-- QUESTION:drag-the-words -->

Drag the correct term into each blank.

According to Leonelli, following a dataset's *[journey]* means asking who *[collected]* it, how it was *[cleaned]* or transformed along the way, and who is able to *[access]* it later. The Bob/Bobby mismatch in this reading is a small, concrete trace of exactly that journey: two different collection moments, with no shared key to guarantee they'd ever line up.

<!-- END QUESTION -->
