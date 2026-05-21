package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

func col(header []string, name string) int {
	for i, h := range header {
		if h == name {
			return i
		}
	}
	return -1
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run inequality_summary.go data/life_course_inequality_panel.csv")
	}

	f, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	rows, err := csv.NewReader(f).ReadAll()
	if err != nil {
		log.Fatal(err)
	}
	if len(rows) < 2 {
		log.Fatal("CSV has no data rows")
	}

	header := rows[0]
	scoreIdx := col(header, "development_score")
	resIdx := col(header, "current_resources")
	burdenIdx := col(header, "current_burden")
	if scoreIdx < 0 || resIdx < 0 || burdenIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	scoreSum := 0.0
	resSum := 0.0
	burdenSum := 0.0

	for _, row := range rows[1:] {
		score, e1 := strconv.ParseFloat(row[scoreIdx], 64)
		res, e2 := strconv.ParseFloat(row[resIdx], 64)
		burden, e3 := strconv.ParseFloat(row[burdenIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil {
			continue
		}
		count++
		scoreSum += score
		resSum += res
		burdenSum += burden
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean development_score: %.4f\n", scoreSum/float64(count))
	fmt.Printf("Mean current_resources: %.4f\n", resSum/float64(count))
	fmt.Printf("Mean current_burden: %.4f\n", burdenSum/float64(count))
}
