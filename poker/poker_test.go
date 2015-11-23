package main

import (
	"fmt"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestParse(t *testing.T) {
	result, _ := ParseLine("a b")
	assert.Equal(t, INVALID, result)
	result, err := ParseLine("HSS7CAC2D7;D9D5C6S5DA")
	assert.Equal(t, INVALID, result)
	result, err = ParseLine("H9S7CAC2D79D5C6S5DA")
	assert.Equal(t, INVALID, result)
	result, err = ParseLine("H9S7CAC2D7;D9D5C6S5DA1")
	assert.Equal(t, INVALID, result)

	result, err = ParseLine("H9S7CAC2D7;D9D5C6S5DA")
	if err != nil {
		fmt.Println(err)
	}
	assert.Equal(t, SECOND_WIN, result)
}

func handScore(hand string) int {
	c := NewContext(hand)
	h, _ := parseHand(c)
	return h.score()
}

func TestScore(t *testing.T) {
	assert.Equal(t, 3, handScore("DJSQSKD5C8"))
	assert.Equal(t, 10, handScore("D2SQSKD5C3"))
	assert.Equal(t, 0, handScore("DAS2S3D4CA"))
	assert.Equal(t, 3, handScore("D5S6S10D9C3"))
}
