mar 25, 2026
- trying to ressurect defsynonym macro memoization
- @make leads to error at (original) line 152 - docreate has been mangled
- I want to create a small test that isolates docreate in an attempt to figure out what is wrong
  - without incurring turnaround delays due to regeneration os dtree
  - dev.bash should temporarily replace @makec with a debug version, then invoke ./@make
- took (...) out of frish.ohm and now the problem is visible: docreate is mangled
- rewired main to skip preoptimize - no errors (as expected)
- λ is an LTmoletter in OhmJS - created rule "kwletter" and used negative match in 'id'
- now, id / name is not doing a lookup
- can I turn on rewrite rule tracing?
- dtree is failing due to latest change in kernel / logging / ???
  - temp.???.nanodsl.mjs opens STDIN which for some reason is set to NON_BLOCKING
  - would creating a temp file be more portable? (Windows, Macos, Linux)
  
calling sequence:
./local/bin/@make [bash script]
  ~/projects/pbp-dev/@make-proto/@make [bash script]
    ~/projects/dtree/@makec [bash script]
	  python 
	    python shells out to ~/projects/dtree/pbp/t2t [bash script]
