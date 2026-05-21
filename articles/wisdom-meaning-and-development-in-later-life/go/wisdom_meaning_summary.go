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
		log.Fatal("Usage: go run wisdom_meaning_summary.go data/wisdom_meaning_later_life_panel.csv")
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
	meaningIdx := col(header, "meaning_score")
	wisdomIdx := col(header, "wisdom_index")
	connectionIdx := col(header, "current_connection")
	reflectionIdx := col(header, "current_reflection")
	healthIdx := col(header, "current_health")
	if meaningIdx < 0 || wisdomIdx < 0 || connectionIdx < 0 || reflectionIdx < 0 || healthIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	meaningSum, wisdomSum, connectionSum, reflectionSum, healthSum := 0.0, 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		meaning, e1 := strconv.ParseFloat(row[meaningIdx], 64)
		wisdom, e2 := strconv.ParseFloat(row[wisdomIdx], 64)
		connection, e3 := strconv.ParseFloat(row[connectionIdx], 64)
		reflection, e4 := strconv.ParseFloat(row[reflectionIdx], 64)
		health, e5 := strconv.ParseFloat(row[healthIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil || e5 != nil {
			continue
		}
		count++
		meaningSum += meaning
		wisdomSum += wisdom
		connectionSum += connection
		reflectionSum += reflection
		healthSum += health
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean meaning_score: %.4f\n", meaningSum/float64(count))
	fmt.Printf("Mean wisdom_index: %.4f\n", wisdomSum/float64(count))
	fmt.Printf("Mean current_connection: %.4f\n", connectionSum/float64(count))
	fmt.Printf("Mean current_reflection: %.4f\n", reflectionSum/float64(count))
	fmt.Printf("Mean current_health: %.4f\n", healthSum/float64(count))
}
