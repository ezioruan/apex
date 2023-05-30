#!/usr/bin/env sh

docker-compose --project-name unit-test up --exit-code-from app --build app
rc=$?
if [ $rc -ne 0 ]
then
  echo "Unit test failed with code $rc"
  exit $rc
fi

echo "Unit test has been excuted successfully"
