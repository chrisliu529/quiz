package main

import (
	"fmt"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestParse(t *testing.T) {
	result, _ := ParseLine("a b")
	assert.Equal(t, INVALID, result)
	result, err := ParseLine("H9S7CAC2D7;D9D5C6S5DA")
	if err != nil {
		fmt.Println(err)
	}
	assert.Equal(t, SECOND_WIN, result)
}
