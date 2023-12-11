# Date time edge case

- reverse ideology meeting Scheduled: 18:00 31/07/23
- alpha 0 meeting Scheduled: 18:00 00/08/23
- should be today's meeting Scheduled: 23:59 01/08/23
- should be tomorrow's meeting Scheduled: 00:01 02/08/23
- theoritically tomorrow's meeting Scheduled: 00:00 02/08/23
- meeting time at 24:00 is not permitted Scheduled: 24:00 02/08/23

# Format edge case

- i got no time Scheduled: 02/08/23
- date disappearance Scheduled: 18:00
- wrong scheduled format Scheduled 18:00 02/08/23
- string between time and date Scheduled: 18:00 hiImString 02/08/23