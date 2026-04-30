package main

import "fmt"

func developmentalScore(care, opportunity, regulation, resilience, risk float64) float64 {
	return 0.22*care + 0.20*opportunity + 0.20*regulation + 0.18*resilience - 0.20*risk
}

func main() {
	score := developmentalScore(0.8, 0.7, 0.65, 0.75, 0.25)
	fmt.Printf("Developmental score: %.3f\n", score)
}
