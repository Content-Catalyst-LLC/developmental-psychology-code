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
		log.Fatal("Usage: go run family_systems_summary.go data/family_systems_panel.csv")
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
	supportIdx := col(header, "family_support_index")
	parentingIdx := col(header, "current_parenting")
	familyIdx := col(header, "current_family")
	stressIdx := col(header, "current_stress")
	if developmentIdx < 0 || supportIdx < 0 || parentingIdx < 0 || familyIdx < 0 || stressIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	developmentSum, supportSum, parentingSum, familySum, stressSum := 0.0, 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		development, e1 := strconv.ParseFloat(row[developmentIdx], 64)
		support, e2 := strconv.ParseFloat(row[supportIdx], 64)
		parenting, e3 := strconv.ParseFloat(row[parentingIdx], 64)
		family, e4 := strconv.ParseFloat(row[familyIdx], 64)
		stress, e5 := strconv.ParseFloat(row[stressIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil || e5 != nil {
			continue
		}
		count++
		developmentSum += development
		supportSum += support
		parentingSum += parenting
		familySum += family
		stressSum += stress
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean development_score: %.4f\n", developmentSum/float64(count))
	fmt.Printf("Mean family_support_index: %.4f\n", supportSum/float64(count))
	fmt.Printf("Mean current_parenting: %.4f\n", parentingSum/float64(count))
	fmt.Printf("Mean current_family: %.4f\n", familySum/float64(count))
	fmt.Printf("Mean current_stress: %.4f\n", stressSum/float64(count))
}
