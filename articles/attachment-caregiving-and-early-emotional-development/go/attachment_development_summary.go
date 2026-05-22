package main
import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)
func idx(h []string, name string) int { for i, v := range h { if v == name { return i } }; return -1 }
func main() {
	if len(os.Args) < 2 { log.Fatal("usage: go run attachment_development_summary.go data/attachment_development_panel.csv") }
	f, err := os.Open(os.Args[1]); if err != nil { log.Fatal(err) }; defer f.Close()
	rows, err := csv.NewReader(f).ReadAll(); if err != nil { log.Fatal(err) }
	h := rows[0]
	cols := []int{idx(h,"regulation_score"),idx(h,"current_care"),idx(h,"current_repair"),idx(h,"current_stress"),idx(h,"caregiving_support_context")}
	names := []string{"regulation_score","current_care","current_repair","current_stress","caregiving_support_context"}
	sums := make([]float64, len(cols))
	for _, r := range rows[1:] { for j, c := range cols { v, _ := strconv.ParseFloat(r[c], 64); sums[j] += v } }
	fmt.Printf("Rows analyzed: %d\n", len(rows)-1)
	for j, name := range names { fmt.Printf("Mean %s: %.4f\n", name, sums[j]/float64(len(rows)-1)) }
}
