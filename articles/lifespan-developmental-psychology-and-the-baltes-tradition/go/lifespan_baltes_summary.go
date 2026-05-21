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
		log.Fatal("Usage: go run lifespan_baltes_summary.go data/lifespan_baltes_panel.csv")
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
	gainsIdx := col(header, "gains")
	lossesIdx := col(header, "losses")
	socIdx := col(header, "soc_index")
	supportIdx := col(header, "current_support")
	if developmentIdx < 0 || gainsIdx < 0 || lossesIdx < 0 || socIdx < 0 || supportIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	developmentSum, gainsSum, lossesSum, socSum, supportSum := 0.0, 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		development, e1 := strconv.ParseFloat(row[developmentIdx], 64)
		gains, e2 := strconv.ParseFloat(row[gainsIdx], 64)
		losses, e3 := strconv.ParseFloat(row[lossesIdx], 64)
		soc, e4 := strconv.ParseFloat(row[socIdx], 64)
		support, e5 := strconv.ParseFloat(row[supportIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil || e5 != nil {
			continue
		}
		count++
		developmentSum += development
		gainsSum += gains
		lossesSum += losses
		socSum += soc
		supportSum += support
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean development_score: %.4f\n", developmentSum/float64(count))
	fmt.Printf("Mean gains: %.4f\n", gainsSum/float64(count))
	fmt.Printf("Mean losses: %.4f\n", lossesSum/float64(count))
	fmt.Printf("Mean soc_index: %.4f\n", socSum/float64(count))
	fmt.Printf("Mean current_support: %.4f\n", supportSum/float64(count))
}
