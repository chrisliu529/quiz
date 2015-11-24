package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestParse(t *testing.T) {
	result, err := ParseLine("")
	assert.Equal(t, INVALID, result)
	assert.Equal(t, "line exhausted", err.Error())

	result, err = ParseLine("a b")
	assert.Equal(t, INVALID, result)
	assert.Equal(t, "bad suit:a", err.Error())

	result, err = ParseLine("HSS7CAC2D7;D9D5C6S5DA")
	assert.Equal(t, INVALID, result)
	assert.Equal(t, "bad rank:S", err.Error())

	result, err = ParseLine("H9S7CAC2D79D5C6S5DA")
	assert.Equal(t, INVALID, result)
	assert.Equal(t, "; expected but 9 found", err.Error())

	result, err = ParseLine("H9S7CAC2D7;D9D5C6S5DA1")
	assert.Equal(t, INVALID, result)
	assert.Equal(t, "eol expected but 1 found", err.Error())

	result, err = ParseLine("H9S7CAC2D7;H9D5C6S5DA")
	assert.Equal(t, INVALID, result)
	assert.Equal(t, "duplicate card found", err.Error())

	result, err = ParseLine("H9S7CAC2S7;D9D5C6S5DA")
	assert.Equal(t, INVALID, result)
	assert.Equal(t, "duplicate card found", err.Error())

	result, err = ParseLine("H9S7CAC2;H9D5C6S5DA")
	assert.Equal(t, INVALID, result)
	assert.Equal(t, "bad suit:;", err.Error())

	result, err = ParseLine("H9S7CAC;H9D5C6S5DA")
	assert.Equal(t, INVALID, result)
	assert.Equal(t, "bad rank:;", err.Error())

	result, err = ParseLine("H9S7CAC2D7;H9D5C6S5D")
	assert.Equal(t, INVALID, result)
	assert.Equal(t, "line exhausted", err.Error())

	result, err = ParseLine("C4C9H4H7CK;C3H6D3S9D8")
	assert.Equal(t, SECOND_WIN, result)

	result, err = ParseLine("DQSJD8C4DA;H3C9H7D6S2")
	assert.Equal(t, FIRST_WIN, result)

	result, err = ParseLine("DQSJD8C4DA;H3C10H7D9S2")
	assert.Equal(t, SECOND_WIN, result)

	result, err = ParseLine("H5SKDQS5HJ;H10SJCQHKS10")
	assert.Equal(t, FIRST_WIN, result)
}

func handScore(hand string) int {
	c := NewContext(hand)
	h, _ := parseHand(c)
	return h.score()
}

func TestScore(t *testing.T) {
	cases := map[string]int{
		"DJSQSKD5C8":     3,
		"D2SQSKD5C3":     10,
		"DAS2S3D4CA":     0,
		"D5S6S10D9C3":    3,
		"D10S10C10DKCQ":  10,
		"D10S10H10DAC10": 1,
		"H5SKDQS5HJ":     10,
		"H10SJCQHKS10":   10,
	}
	for hand, score := range cases {
		assert.Equal(t, score, handScore(hand))
	}
}

func cardVal(card string) int {
	c := NewContext(card)
	ci, _ := parseCard(c)
	return ci.val()
}

func TestCard(t *testing.T) {
	assert.True(t, cardVal("SK") > cardVal("HK"))
	assert.True(t, cardVal("DK") > cardVal("SQ"))
}
