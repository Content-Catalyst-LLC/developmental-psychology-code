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
		log.Fatal("Usage: go run accessibility_summary.go data/disability_neurodivergence_panel.csv")
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
	participationIdx := col(header, "participation_score")
	accessIdx := col(header, "current_access")
	barrierIdx := col(header, "current_barrier")
	if developmentIdx < 0 || participationIdx < 0 || accessIdx < 0 || barrierIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	developmentSum, participationSum, accessSum, barrierSum := 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		development, e1 := strconv.ParseFloat(row[developmentIdx], 64)
		participation, e2 := strconv.ParseFloat(row[participationIdx], 64)
		access, e3 := strconv.ParseFloat(row[accessIdx], 64)
		barrier, e4 := strconv.ParseFloat(row[barrierIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil {
			continue
		}
		count++
		developmentSum += development
		participationSum += participation
		accessSum += access
		barrierSum += barrier
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean development_score: %.4f\n", developmentSum/float64(count))
	fmt.Printf("Mean participation_score: %.4f\n", participationSum/float64(count))
	fmt.Printf("Mean current_access: %.4f\n", accessSum/float64(count))
	fmt.Printf("Mean current_barrier: %.4f\n", barrierSum/float64(count))
}
