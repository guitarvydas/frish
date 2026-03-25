mar 25, 2026
- trying to ressurect defsynonym macro memoization
- @make leads to error at (original) line 152 - docreate has been mangled
- I want to create a small test that isolates docreate in an attempt to figure out what is wrong
  - without incurring turnaround delays due to regeneration os dtree
  - dev.bash should temporarily replace @makec with a debug version, then invoke ./@make
