#!/usr/bin/env bats

setup() {
  mkdir -p tmp
  echo "debug log entry" > tmp/debug.txt
  echo "log error" > tmp/error.txt
}

teardown() {
  rm -rf tmp
}

@test "finds files by name fragment" {
  run ./bin/shellman find_files tmp --name debug
  [ "$status" -eq 0 ]
  [[ "$output" =~ "debug.txt" ]]
}

@test "finds files by content" {
  run ./bin/shellman find_files tmp --content error
  [ "$status" -eq 0 ]
  [[ "$output" =~ "error.txt" ]]
}
