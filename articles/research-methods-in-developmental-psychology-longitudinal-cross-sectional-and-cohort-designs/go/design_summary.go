package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

func findColumn(header []string, name string) int {
	for i, col := range header {
		if col == name {
			return i
		}
	}
	return -1
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run design_summary.go data/developmental_design_panel.csv")
	}

	file, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	rows, err := reader.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	if len(rows) < 2 {
		log.Fatal("CSV has no data rows")
	}

	header := rows[0]
	scoreIdx := findColumn(header, "development_score")
	observedIdx := findColumn(header, "observed")
	ageIdx := findColumn(header, "age")

	if scoreIdx < 0 || observedIdx < 0 || ageIdx < 0 {
		log.Fatal("Required columns not found")
	}

	count := 0
	scoreSum := 0.0
	ageSum := 0.0

	for _, row := range rows[1:] {
		observed, err := strconv.Atoi(row[observedIdx])
		if err != nil || observed != 1 {
			continue
		}

		score, err1 := strconv.ParseFloat(row[scoreIdx], 64)
		age, err2 := strconv.ParseFloat(row[ageIdx], 64)

		if err1 != nil || err2 != nil {
			continue
		}

		count++
		scoreSum += score
		ageSum += age
	}

	if count == 0 {
		log.Fatal("No observed rows found")
	}

	fmt.Printf("Observed rows analyzed: %d\n", count)
	fmt.Printf("Mean age: %.4f\n", ageSum/float64(count))
	fmt.Printf("Mean development_score: %.4f\n", scoreSum/float64(count))
}
