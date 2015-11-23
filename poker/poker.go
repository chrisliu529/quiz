package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

type Results struct {
	first_win  int
	second_win int
	invalid    int
}

const (
	_ = iota
	//win status
	FIRST_WIN
	SECOND_WIN
	INVALID

	//suits
	DIAMOND
	CLUB
	HEART
	SPADE

	N_CARDS = 5
	OK      = 0
)

type Context struct {
	pos        int
	expression string
}

func NewContext(line string) *Context {
	s := strings.TrimSpace(line)
	return &Context{pos: 0, expression: s}
}

func (c *Context) cur() (str string, err error) {
	if c.pos < len(c.expression) {
		return string(c.expression[c.pos]), nil
	}
	return str, errors.New("line exhuasted")
}

func (c *Context) forward() {
	c.pos++
}

type Card struct {
	suit int
	rank int
}

var str2suit map[string]int = map[string]int{
	"S": SPADE,
	"H": HEART,
	"C": CLUB,
	"D": DIAMOND,
}

var str2rank map[string]int = map[string]int{
	"A": 1,
	"J": 10,
	"Q": 10,
	"K": 10,
}

type Hand struct {
	cards   []*Card
	n       int
	__score int
}

func NewHand() *Hand {
	return &Hand{cards: make([]*Card, N_CARDS), n: 0, __score: -1}
}

func (h *Hand) addCard(c *Card) error {
	if h.n >= N_CARDS {
		return errors.New("too many cards")
	}
	h.cards[h.n] = c
	h.n++
	return nil
}

func (h *Hand) sum() int {
	s := 0
	for _, card := range h.cards {
		s += card.rank
	}
	return s
}

func (h *Hand) score() int {
	if h.__score < 0 {
		h.__score = h._score()
	}
	return h.__score
}

func (h *Hand) _score() int {
	s := h.sum()
	for i := 0; i < h.n-1; i++ {
		r := h.cards[i].rank
		for j := i + 1; j < h.n; j++ {
			ri := r
			r += h.cards[j].rank
			t := s - r
			if t%10 == 0 {
				r2 := r - 10
				if r2 > 0 {
					return r2
				}
				return r
			}
			r = ri
		}
	}
	return 0
}

func parseSuit(c *Context) (suit int, err error) {
	str, err := c.cur()
	if err != nil {
		return suit, err
	}
	if suit, found := str2suit[str]; found {
		c.forward()
		return suit, nil
	}
	return suit, errors.New("bad suit:" + str)
}

func parseRank(c *Context) (rank int, err error) {
	str, err := c.cur()
	if err != nil {
		return rank, err
	}
	if str == "1" {
		c.forward()
		str2, err := c.cur()
		if err != nil {
			return rank, err
		}
		if str2 == "0" {
			c.forward()
			return 10, nil
		}
		return 0, errors.New("bad rank: 1" + str2)
	} else if i, err := strconv.Atoi(str); err == nil {
		c.forward()
		return i, nil
	} else if i, found := str2rank[str]; found {
		c.forward()
		return i, nil
	}
	return rank, errors.New("bad rank:" + str)
}

func parseCard(c *Context) (card *Card, err error) {
	var r int
	s, err := parseSuit(c)
	if err != nil {
		goto Error
	}
	r, err = parseRank(c)
	if err != nil {
		goto Error
	}
	return &Card{suit: s, rank: r}, nil
Error:
	return card, err
}

func parseHand(c *Context) (*Hand, error) {
	h := NewHand()
	for i := 0; i < N_CARDS; i++ {
		card, err := parseCard(c)
		if err != nil {
			return nil, err
		}
		if err = h.addCard(card); err != nil {
			return nil, err
		}
	}
	return h, nil
}

func parseSep(c *Context) (ignore int, err error) {
	s, err := c.cur()
	if err != nil {
		return ignore, err
	}
	if s == ";" {
		c.forward()
		return ignore, nil
	}
	return ignore, errors.New("; expected but " + s + " found")
}

func parseEnd(c *Context) (ignore int, err error) {
	s, err := c.cur()
	if err == nil {
		return ignore, errors.New("eol expected but " + s + " found")
	}
	return ignore, nil
}

func compareHands(h1 *Hand, h2 *Hand) (result int, err error) {
	s1 := h1.score()
	s2 := h2.score()
	if s1 > s2 {
		return FIRST_WIN, nil
	}
	return SECOND_WIN, nil
}

func ParseLine(line string) (int, error) {
	c := NewContext(line)
	h1, err := parseHand(c)
	if err != nil {
		return INVALID, err
	}
	if _, err := parseSep(c); err != nil {
		return INVALID, err
	}
	h2, err := parseHand(c)
	if err != nil {
		return INVALID, err
	}
	if _, err := parseEnd(c); err != nil {
		return INVALID, err
	}
	return compareHands(h1, h2)
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func analyzeRecords(filename string) *Results {
	text, err := ioutil.ReadFile(filename)
	check(err)
	lines := strings.Split(string(text), "\n")
	res := &Results{first_win: 0, second_win: 0, invalid: 0}
	for i := range lines {
		r, err := ParseLine(lines[i])
		if err != nil {
			res.invalid++
		}
		switch r {
		case FIRST_WIN:
			res.first_win++
		case SECOND_WIN:
			res.second_win++
		}
	}
	return res
}

func (r *Results) String() string {
	return fmt.Sprintf(
		"Leon won %d times\n"+
			"Judy won %d times",
		r.first_win, r.second_win)
}

func main() {
	res := analyzeRecords("LJ-poker.txt")
	fmt.Println(res)
}
