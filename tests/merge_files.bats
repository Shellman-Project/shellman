#!/usr/bin/env bats

setup() {
  mkdir -p tmp
  echo "one" > tmp/a.txt
  echo "two" > tmp/b.txt
  echo "three" > tmp/c.txt
}

teardown() {
  rm -rf tmp logs
}

@test "merges .txt files into one file" {
  run ./bin/shellman merge_files --ext txt --path tmp --out tmp/merged_test.txt
  [ "$status" -eq 0 ]
  [[ "$output" == *"Merge complete: tmp/merged_test.txt"* ]]
  [ -f "tmp/merged_test.txt" ]
  grep -q "one" tmp/merged_test.txt
  grep -q "three" tmp/merged_test.txt
}

@test "adds filename headers when --header is used" {
  run ./bin/shellman merge_files --ext txt --path tmp --out tmp/with_header.txt --header
  [ "$status" -eq 0 ]
  grep -q "=== .*a.txt ===" tmp/with_header.txt
  grep -q "=== .*b.txt ===" tmp/with_header.txt
  grep -q "one" tmp/with_header.txt
}

@test "sorts files alphabetically when --sort is used" {
  echo "zzz" > tmp/z.txt
  echo "aaa" > tmp/a.txt
  echo "mmm" > tmp/m.txt

  run ./bin/shellman merge_files --ext txt --path tmp --out tmp/sorted.txt --sort

  [ "$status" -eq 0 ]

  FIRST=$(grep -n "aaa" tmp/sorted.txt | cut -d: -f1)
  SECOND=$(grep -n "mmm" tmp/sorted.txt | cut -d: -f1)
  THIRD=$(grep -n "zzz" tmp/sorted.txt | cut -d: -f1)

  (( FIRST < SECOND ))
  (( SECOND < THIRD ))
}

@test "uses both --header and --sort together correctly" {
  echo "ccc" > tmp/c.txt
  echo "aaa" > tmp/a.txt
  echo "bbb" > tmp/b.txt

  run ./bin/shellman merge_files --ext txt --path tmp --out tmp/combined.txt --header --sort
  [ "$status" -eq 0 ]

  HEADERS=($(grep -n "^=== " tmp/combined.txt | cut -d: -f1))
  LINES=($(grep -n -e "aaa" -e "bbb" -e "ccc" tmp/combined.txt | cut -d: -f1))

  [[ $(sed -n "${HEADERS[0]}p" tmp/combined.txt) == *"a.txt"* ]]
  [[ $(sed -n "${HEADERS[1]}p" tmp/combined.txt) == *"b.txt"* ]]
  [[ $(sed -n "${HEADERS[2]}p" tmp/combined.txt) == *"c.txt"* ]]

  (( LINES[0] < LINES[1] ))
  (( LINES[1] < LINES[2] ))
}
