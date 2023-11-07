#!/bin/bash

#
# Mercurial and Named Branches
#

cd /tmp
if [ -d named_branches ]; then
    rm -rf named_branches
fi

hg init named_branches
cd named_branches

hg summary

echo 'zero' > default.txt
hg add
hg commit -m zero -d '0 0' --user Fulano

hg branch

hg branch stable
hg summary

echo 'one' > stable.txt
hg add
hg commit -m one -d '0 0' --user Beltrano

echo 'two' >> stable.txt
hg commit -m two -d '0 0' --user Beltrano

hg update default
echo 'three' >> default.txt
hg commit -m tres -d '0 0' --user Fulano

hg log -G
hg log -G --template '{rev}:{node|short} | {branch}'

hg branches


hg merge stable
hg commit -m four -d '0 0' --user Beltrano

hg update 3
hg branch bug
echo 'five' > bug.txt
hg add
hg commit -m five -d '0 0' --user Fulano

echo 'six' >> bug.txt
hg commit -m six -d '0 0' --user Fulano

hg update default
hg merge bug
hg commit -m seven -d '0 0' --user Fulano

hg up 0
hg branch feature
echo 'eigth' > feature.txt
hg add
hg commit -m eigth -d '0 0' --user Fulano

hg merge bug
hg commit -m nine -d '0 0' --user Fulano

echo -e '\n\n========\ndefault\n========'
hg log -Gqb default
echo -e '\n\n=======\nfeature\n======='
hg log -Gqb feature
echo -e '\n\n===\nbug\n==='
hg log -Gqb bug
echo -e '\n\n======\nstable\n======'
hg log -Gqb stable