package main

import (
	"flag"
	"fmt"
	"golang.org/x/text/language"
	"golang.org/x/text/message"
	"runtime"
	"time"
)

type Person struct {
	firstName string
	lastName  string
	age       int
}

func NewPerson(firstName, lastName string, age int) *Person {
	return &Person{
		firstName: firstName,
		lastName:  lastName,
		age:       age,
	}
}

func (p Person) GetFullName() string {
	return p.firstName + " " + p.lastName
}

func (p *Person) IncreaseAge() {
	p.age++
}

func printStats(start time.Time, objectsCreated int) {
	elapsed := time.Since(start)

	var mem runtime.MemStats
	runtime.ReadMemStats(&mem)
	totalMemoryAllocated := mem.TotalAlloc
	totalMemoryMB := float64(totalMemoryAllocated / (1024 * 1024))

	p := message.NewPrinter(language.English)
	p.Printf("%d Person in %s. Memory: %.2f MB.\n",
		objectsCreated, elapsed, totalMemoryMB)

}

func createPersons(start time.Time, total int, ch chan int) {
	Persons := make([]*Person, total)
	for i := 1; i <= total; i++ {
		person := NewPerson("John", "Doe", 30)
		_ = person.GetFullName()
		person.IncreaseAge()
		Persons[i-1] = person

		if i%1000000 == 0 {
			printStats(start, i)
		}
	}
	if ch != nil {
		ch <- total
	}
}

func main() {
	var useMultipleCores bool
	flag.BoolVar(&useMultipleCores, "multicore", false,
		"Use multiple CPU cores")
	flag.Parse()

	personsNum := 4000000
	start := time.Now()

	if useMultipleCores {
		numCPU := runtime.NumCPU()
		runtime.GOMAXPROCS(numCPU)

		ch := make(chan int, numCPU)
		for i := 0; i < numCPU; i++ {
			go createPersons(start, personsNum/numCPU, ch)
		}

		for i := 0; i < numCPU; i++ {
			<-ch
		}

		close(ch)
	} else {
		createPersons(start, personsNum, nil)
	}

	fmt.Printf("* Total time: %s\n", time.Since(start))
}
