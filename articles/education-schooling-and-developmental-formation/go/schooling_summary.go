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
		log.Fatal("Usage: go run schooling_summary.go data/schooling_development_panel.csv")
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
	connectednessIdx := col(header, "connectedness_score")
	teacherIdx := col(header, "current_teacher")
	peerIdx := col(header, "current_peer")
	stressIdx := col(header, "current_stress")
	if developmentIdx < 0 || connectednessIdx < 0 || teacherIdx < 0 || peerIdx < 0 || stressIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	developmentSum, connectednessSum, teacherSum, peerSum, stressSum := 0.0, 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		development, e1 := strconv.ParseFloat(row[developmentIdx], 64)
		connectedness, e2 := strconv.ParseFloat(row[connectednessIdx], 64)
		teacher, e3 := strconv.ParseFloat(row[teacherIdx], 64)
		peer, e4 := strconv.ParseFloat(row[peerIdx], 64)
		stress, e5 := strconv.ParseFloat(row[stressIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil || e5 != nil {
			continue
		}
		count++
		developmentSum += development
		connectednessSum += connectedness
		teacherSum += teacher
		peerSum += peer
		stressSum += stress
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean development_score: %.4f\n", developmentSum/float64(count))
	fmt.Printf("Mean connectedness_score: %.4f\n", connectednessSum/float64(count))
	fmt.Printf("Mean current_teacher: %.4f\n", teacherSum/float64(count))
	fmt.Printf("Mean current_peer: %.4f\n", peerSum/float64(count))
	fmt.Printf("Mean current_stress: %.4f\n", stressSum/float64(count))
}
