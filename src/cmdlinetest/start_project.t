Create project and check the expected files are there

  $ ls
  $ resco start-project testproject
  $ tree -ifF
  .
  ./fabfile.py
  ./README.md
  ./requirements/
  ./requirements/all.txt
  ./requirements/local.txt
  ./requirements/remote.txt
  ./scripts/
  ./scripts/analysis/
  ./scripts/behaviour/
  ./scripts/figures/
  ./scripts/theory/
  ./scripts/tools/
  ./target/
  ./target/results/
  ./target/results/analysis/
  ./target/results/behaviour/
  ./target/results/figures/
  ./target/results/theory/
  ./testproject/
  ./testproject/__init__.py
  ./unittests/
  
  15 directories, 6 files
