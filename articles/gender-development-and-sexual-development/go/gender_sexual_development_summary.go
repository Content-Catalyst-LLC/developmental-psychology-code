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
		log.Fatal("Usage: go run gender_sexual_development_summary.go data/gender_sexual_development_panel.csv")
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
	adjustmentIdx := col(header, "adjustment_score")
	protectiveIdx := col(header, "protective_context")
	stigmaIdx := col(header, "current_stigma")
	familyIdx := col(header, "current_family_support")
	consentIdx := col(header, "current_consent_knowledge")
	if adjustmentIdx < 0 || protectiveIdx < 0 || stigmaIdx < 0 || familyIdx < 0 || consentIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	adjustmentSum, protectiveSum, stigmaSum, familySum, consentSum := 0.0, 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		adjustment, e1 := strconv.ParseFloat(row[adjustmentIdx], 64)
		protective, e2 := strconv.ParseFloat(row[protectiveIdx], 64)
		stigma, e3 := strconv.ParseFloat(row[stigmaIdx], 64)
		family, e4 := strconv.ParseFloat(row[familyIdx], 64)
		consent, e5 := strconv.ParseFloat(row[consentIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil || e5 != nil {
			continue
		}
		count++
		adjustmentSum += adjustment
		protectiveSum += protective
		stigmaSum += stigma
		familySum += family
		consentSum += consent
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean adjustment_score: %.4f\n", adjustmentSum/float64(count))
	fmt.Printf("Mean protective_context: %.4f\n", protectiveSum/float64(count))
	fmt.Printf("Mean current_stigma: %.4f\n", stigmaSum/float64(count))
	fmt.Printf("Mean current_family_support: %.4f\n", familySum/float64(count))
	fmt.Printf("Mean current_consent_knowledge: %.4f\n", consentSum/float64(count))
}
