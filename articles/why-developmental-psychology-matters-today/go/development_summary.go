package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run development_summary.go data/developmental_panel.csv")
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
	scoreIndex := -1
	for i, name := range header {
		if name == "development_score" {
			scoreIndex = i
			break
		}
	}
	if scoreIndex < 0 {
		log.Fatal("development_score column not found")
	}

	count := 0
	sum := 0.0
	minScore := 1e18
	maxScore := -1e18

	for _, row := range rows[1:] {
		score, err := strconv.ParseFloat(row[scoreIndex], 64)
		if err != nil {
			continue
		}
		count++
		sum += score
		if score < minScore {
			minScore = score
		}
		if score > maxScore {
			maxScore = score
		}
	}

	if count == 0 {
		log.Fatal("No valid development_score values found")
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean development_score: %.4f\n", sum/float64(count))
	fmt.Printf("Minimum development_score: %.4f\n", minScore)
	fmt.Printf("Maximum development_score: %.4f\n", maxScore)
}
