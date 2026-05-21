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
		log.Fatal("Usage: go run plasticity_summary.go data/genes_environment_plasticity_panel.csv")
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
	developmentIdx := col(header, "development_score")
	stressIdx := col(header, "embedded_stress")
	supportIdx := col(header, "embedded_support")
	careIdx := col(header, "current_care")
	currentStressIdx := col(header, "current_stress")
	if developmentIdx < 0 || stressIdx < 0 || supportIdx < 0 || careIdx < 0 || currentStressIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	developmentSum, stressSum, supportSum, careSum, currentStressSum := 0.0, 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		development, e1 := strconv.ParseFloat(row[developmentIdx], 64)
		stress, e2 := strconv.ParseFloat(row[stressIdx], 64)
		support, e3 := strconv.ParseFloat(row[supportIdx], 64)
		care, e4 := strconv.ParseFloat(row[careIdx], 64)
		currentStress, e5 := strconv.ParseFloat(row[currentStressIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil || e5 != nil {
			continue
		}
		count++
		developmentSum += development
		stressSum += stress
		supportSum += support
		careSum += care
		currentStressSum += currentStress
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean development_score: %.4f\n", developmentSum/float64(count))
	fmt.Printf("Mean embedded_stress: %.4f\n", stressSum/float64(count))
	fmt.Printf("Mean embedded_support: %.4f\n", supportSum/float64(count))
	fmt.Printf("Mean current_care: %.4f\n", careSum/float64(count))
	fmt.Printf("Mean current_stress: %.4f\n", currentStressSum/float64(count))
}
