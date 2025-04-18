#!/usr/bin/env bats

setup() {
  mkdir -p tmp/zippable
  echo "log line 1" > tmp/zippable/file1.log
}

teardown() {
  rm -rf tmp zips
}

@test "creates a zip archive from files in folder" {
  run ./bin/shellman zip_batch --path tmp/zippable --ext log --output zips --name test_
  [ "$status" -eq 0 ]

  ZIPFILE=$(find zips -name 'test_*.zip' | head -n 1)
  [ -f "$ZIPFILE" ]

  unzip -l "$ZIPFILE" | grep -q "file1.log"
}

@test "creates separate zip for each folder when --per-folder is used" {
  mkdir -p tmp/project1 tmp/project2
  echo "a" > tmp/project1/file1.txt
  echo "b" > tmp/project2/file2.txt

  run ./bin/shellman zip_batch --path tmp --per-folder --output zips --name folder_

  [ "$status" -eq 0 ]
  [ -f "zips/folder_project1.zip" ]
  [ -f "zips/folder_project2.zip" ]

  unzip -l zips/folder_project1.zip | grep -q "file1.txt"
  unzip -l zips/folder_project2.zip | grep -q "file2.txt"
}

@test "creates password-protected zip archive" {
  echo "secret data" > tmp/file_secret.txt

  run ./bin/shellman zip_batch --path tmp --ext txt --output zips --name secure_ --password test123
  [ "$status" -eq 0 ]

  ZIPFILE=$(find zips -name 'secure_*.zip' | head -n 1)
  [ -f "$ZIPFILE" ]

  unzip -P test123 -l "$ZIPFILE" | grep -q "file_secret.txt"
}
