# Showing Scheduler

Clone of Orion trsoxh module 2.

## Confirmation email (send when slot locked)

**Subject:** Showing confirmed — [ADDRESS] on [DATE] at [TIME]

> Hi [NAME],
>
> Your showing is confirmed for **[DATE] at [TIME]** at **[ADDRESS]**.
>
> Please bring a valid photo ID. The showing takes about **15 minutes**. If you need to reschedule, reply at least 24 hours ahead.
>
> Parking: [INSTRUCTIONS]. Text [PHONE] when you arrive.
>
> — [YOUR NAME]

## 24-hour reminder (text or email)

> Reminder: property showing tomorrow [DATE] [TIME] at [ADDRESS]. Reply C to confirm or R to reschedule.

## No-show follow-up (2 hours after slot)

> Hi [NAME], we missed you at today's showing for [ADDRESS]. Still interested? Reply with two times that work this week and I'll hold a slot.

## Batch showing script (high-demand unit)

Schedule 15-minute blocks back-to-back (e.g. 2:00, 2:20, 2:40). Open door once per block; group max 2 parties if fire code allows.

**Group intro (read once):**
> Thanks for coming. This is a 15-minute self-guided walkthrough. I'll be in the [location] if you have questions. Application link is on the counter — first qualified applicant gets priority.

## AI prompt — schedule from inquiry thread

```plaintext
Prospect messages: "[PASTE THREAD]"
Available showing windows: [LIST 3–5 SLOTS]
Write a scheduling reply offering two slots, confirming ID requirement, and 15-minute duration. Under 120 words.
```
