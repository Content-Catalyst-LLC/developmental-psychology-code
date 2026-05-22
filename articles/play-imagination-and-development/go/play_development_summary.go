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
	if len(os.Args) < 2 { log.Fatal("usage: go run play_development_summary.go data/play_development_panel.csv") }
	f, err := os.Open(os.Args[1]); if err != nil { log.Fatal(err) }; defer f.Close()
	rows, err := csv.NewReader(f).ReadAll(); if err != nil { log.Fatal(err) }
	h := rows[0]
	cols := []int{idx(h,"development_score"),idx(h,"current_pretend"),idx(h,"current_social_play"),idx(h,"current_outdoor"),idx(h,"play_support_context"),idx(h,"play_restriction")}
	names := []string{"development_score","current_pretend","current_social_play","current_outdoor","play_support_context","play_restriction"}
	sums := make([]float64, len(cols))
	for _, r := range rows[1:] { for j, c := range cols { v, _ := strconv.ParseFloat(r[c], 64); sums[j] += v } }
	fmt.Printf("Rows analyzed: %d\n", len(rows)-1)
	for j, name := range names { fmt.Printf("Mean %s: %.4f\n", name, sums[j]/float64(len(rows)-1)) }
}
