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

  $ echo "print('Hello world')" > scripts/tools/hello.py
  $ fab -H localhost -p $PASSWORD update_venv > silence
  $ fab -H localhost -p $PASSWORD run_script:tools/hello.py
  
  -* (re)
  Ran 0 tests in 0.000s
  
  OK
  [localhost] Executing task 'run_script'
  [localhost] local: python -m unittest discover -s unittests/ -p '*tests.py'
  [localhost] put: testproject/__init__.py -> testproject-wd/testproject/__init__.py
  [localhost] put: scripts/tools/hello.py -> testproject-wd/scripts/tools/hello.py
  [localhost] run: PYTHONPATH=. python scripts/tools/hello.py
  [localhost] out: Hello world
  [localhost] out: 
  
  
  Done.
  Disconnecting from localhost... done.
