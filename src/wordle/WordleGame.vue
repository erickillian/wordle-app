<template>
    <div>
        <h1 class="header">Convergle</h1>
        <div class="alert-container" data-alert-container></div>
        <div data-guess-grid class="guess-grid">
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
            <div class="tile"></div>
        </div>
        <div data-keyboard class="keyboard">
            <button class="key" data-key="Q">Q</button>
            <button class="key" data-key="W">W</button>
            <button class="key" data-key="E">E</button>
            <button class="key" data-key="R">R</button>
            <button class="key" data-key="T">T</button>
            <button class="key" data-key="Y">Y</button>
            <button class="key" data-key="U">U</button>
            <button class="key" data-key="I">I</button>
            <button class="key" data-key="O">O</button>
            <button class="key" data-key="P">P</button>
            <div class="space"></div>
            <button class="key" data-key="A">A</button>
            <button class="key" data-key="S">S</button>
            <button class="key" data-key="D">D</button>
            <button class="key" data-key="F">F</button>
            <button class="key" data-key="G">G</button>
            <button class="key" data-key="H">H</button>
            <button class="key" data-key="J">J</button>
            <button class="key" data-key="K">K</button>
            <button class="key" data-key="L">L</button>
            <div class="space"></div>
            <button data-enter class="key large">Enter</button>
            <button class="key" data-key="Z">Z</button>
            <button class="key" data-key="X">X</button>
            <button class="key" data-key="C">C</button>
            <button class="key" data-key="V">V</button>
            <button class="key" data-key="B">B</button>
            <button class="key" data-key="N">N</button>
            <button class="key" data-key="M">M</button>
            <button data-delete class="key large">
                <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
                    <path fill="var(--color-tone-1)"
                        d="M22 3H7c-.69 0-1.23.35-1.59.88L0 12l5.41 8.11c.36.53.9.89 1.59.89h15c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H7.07L2.4 12l4.66-7H22v14zm-11.59-2L14 13.41 17.59 17 19 15.59 15.41 12 19 8.41 17.59 7 14 10.59 10.41 7 9 8.41 12.59 12 9 15.59z">
                    </path>
                </svg>
            </button>
        </div>
    </div>
</template>
<style src="./styles.css" >
</style>
        

<script>
import { mapActions, mapState } from 'vuex';

// CONSTANTS
const WORD_LENGTH = 5;
const FLIP_ANIMATION_DURATION = 750
const DANCE_ANIMATION_DURATION = 500

export default {
    name: "wordle",
    // components: { SimpleCard, LeadersCard, BigNumberCard },
    mounted() {
        document.addEventListener("click", this.handleMouseClick);
        document.addEventListener("keydown", this.handleKeyPress);
        this.guessGrid = this.$el.querySelector("[data-guess-grid]");
        this.keyboard = this.$el.querySelector("[data-keyboard]");
        this.alertContainer = this.$el.querySelector("[data-alert-container]"); // get the empty div container for alerts
        this.targetWord = "hooll";
        this.targetWords = ["hello", "howdy", "hooll", "hoolo"];
        this.status();
    },
    computed: {
        initial_load() {
            return this.$store.state.wordle.initial_load;
        },
        guess_ok() {
            return this.$store.state.wordle.guess_ok;
        },
        guess_error() {
            return this.$store.state.wordle.guess_error;
        },
    },
    watch: {
        initial_load() {
            this.initialGuesses()
        },
        guess_ok() {
            if (this.$store.state.wordle.guess_ok == true) {
                this.guessOk()
                this.$store.commit('wordle/WORDLE_GUESS_RESPONDED')
            }  
        },
        guess_error() {
            if (this.$store.state.wordle.guess_error == true) {
                this.guessError()
                this.$store.commit('wordle/WORDLE_GUESS_RESPONDED')
            }  
        },
    },

    data() {
        return {
            statusLoaded: this.$store.state.wordle.status_loading,
            inputs: {
                guess: '',
            },
        };
    },
    // mounted: this.startInteraction(),
    methods: {
        ...mapActions('wordle', [
            'guess',
            'status',
        ]),
        ...mapState({
            wordle: state=> state.wordle
        }),
        startInteraction() { // start listening for clicks and keypresses
            document.addEventListener("click", this.handleMouseClick);
            document.addEventListener("keydown", this.handleKeyPress);
        },
        stopInteraction() { // remove the event listeners for clicks and keypresses, effectively making the user unable to interact or type anything
            document.removeEventListener("click", this.handleMouseClick);
            document.removeEventListener("keydown", this.handleKeyPress);
        },
        handleMouseClick(e) {
            if (e.target.matches("[data-key")) { // if event target is a key, press that key
                this.pressKey(e.target.dataset.key);
                return;
            }

            if (e.target.matches("[data-enter]")) { // if user clicks enter, submit the guess
                this.submitGuess();
                return;
            }

            if (e.target.matches("[data-delete]")) { // if user clicks delete, remove that key
                this.deleteKey();
                return;
            }
        },
        handleKeyPress(e) {
            if (e.key === "Enter") { // if the key is enter, submit guess
                this.submitGuess()
                return
            }

            if (e.key === "Backspace" || e.key === "Delete") { // if user presses backspace or delete, delete key
                this.deleteKey()
            }

            if (e.key.match(/^[a-z]$/)) { // regex for one single letter between a and z
                this.pressKey(e.key)
                return
            }
        },
        pressKey(key) { // add key to first tile in grid
            const activeTiles = this.getActiveTiles() // get array of active tiles
            if (activeTiles.length >= WORD_LENGTH) return // make sure that user cannot keep typing after 5 letters
            
            const nextTile = this.guessGrid.querySelector(":not([data-letter])") // returns the first tile that doesn't have a value
            nextTile.dataset.letter = key.toLowerCase() // add the letter to the tile's dataset
            nextTile.textContent = key // make the html the key
            nextTile.dataset.state = "active" // set it to active
            this.inputs.guess += key.toLowerCase()
        },
        deleteKey() {
            const activeTiles = this.getActiveTiles() // get array of active tiles
            const lastTile = activeTiles[activeTiles.length - 1] // get the last active tile
            if (!lastTile) return // if that tile doesn't have any content, return
            lastTile.textContent = "" // set the text content to an empty string
            delete lastTile.dataset.state // delete active state
            delete lastTile.dataset.letter // delete letter dataset
            this.inputs.guess = this.inputs.guess.slice(0, -1)
        },
        getActiveTiles() {
            return this.guessGrid.querySelectorAll('[data-state="active"]')
            // return all the tiles that have the state of active
        },
        submitGuess() {
            const activeTiles = [...this.getActiveTiles()] // get the array of active tiles
            if (activeTiles.length !== WORD_LENGTH) { // if the guess isn't long enough, can't submit it!
                this.showAlert("Not enough letters!")
                this.shakeTiles(activeTiles)
                return
            }
            const guess = activeTiles.reduce((word, tile) => { // sum the array of individual letters into a string
                return word + tile.dataset.letter
            }, "") // returns a string

            this.guess({ guess: guess });
            this.stopInteraction()
            // activeTiles.forEach((...params) => this.flipTile(...params, guess)) // flip tile animation
        },
        initialGuesses() {
            if (this.$store.state.wordle.status_loading == false) {
                const guess_history = this.$store.state.wordle.info.guess_history;
                const correct = this.$store.state.wordle.info.correct;
                for (var i=0; i < guess_history.length; i++) {
                    const nextTile = this.guessGrid.querySelector(":not([data-letter])");
                    nextTile.textContent = guess_history[i].toLowerCase()
                    nextTile.dataset.letter = guess_history[i].toLowerCase()
                    if (correct[i] == "0") {
                        nextTile.dataset.state = "wrong"
                    }
                    if (correct[i] == "1") {
                        nextTile.dataset.state = "wrong-location"
                    }
                    if (correct[i] == "2") {
                        nextTile.dataset.state = "correct"
                    }
                    
                    setTimeout(() => {
                        nextTile.classList.add("bounce")
                        nextTile.addEventListener(
                            "animationend",
                            () => {
                                nextTile.classList.remove("bounce")
                            },
                            { once: true }
                        )
                    }, (i * DANCE_ANIMATION_DURATION*.75) / 7)
                }
                if (this.$store.state.wordle.info.solved == true) {
                    console.log("solved")
                    this.stopInteraction()
                }
            }
        },
        guessOk() {
            const guess = this.$store.state.wordle.info.guess_history.slice(-WORD_LENGTH);
            const correct = this.$store.state.wordle.info.correct.slice(-WORD_LENGTH);
            this.startInteraction()

            const activeTiles = [...this.getActiveTiles()]
            activeTiles.forEach((...params) => this.flipTile(...params, guess, correct)) // flip tile animation
            if (this.$store.state.wordle.info.solved == true) {
                console.log("solved")
                this.stopInteraction()
            } else {
                this.startInteraction()
            }

        },
        guessError() {
            this.startInteraction()
            const activeTiles = [...this.getActiveTiles()]
            this.shakeTiles(activeTiles)// flip tile animation
            this.showAlert("Guess Error")

        },
        flipTile(tile, index, array, guess, correct) {
            const letter = tile.dataset.letter           
            const key = this.keyboard.querySelector(`[data-key="${letter}"i]`) // get each key - the i makes it case insensitivehel
            setTimeout(() => {
                tile.classList.add("flip")
            }, index * FLIP_ANIMATION_DURATION / 2)

            tile.addEventListener("transitionend", () => {
                tile.classList.remove("flip") // remvoe flip class for animation
                if (correct[index] === "2") {
                    tile.dataset.state = "correct"
                    key.classList.add("correct") // while flipping, if it's the right location and right letter, add correct class
                } else if (correct[index] === "1") { // otherwise if word includes letter, add wrong location class
                    tile.dataset.state = "wrong-location"
                    key.classList.add("wrong-location")
                } else if (correct[index] === "0") { // else add wrong class
                    tile.dataset.state = "wrong"
                    key.classList.add("wrong")
                }

                if (index === array.length - 1) { // if last tile, user can start interacting again
                    tile.addEventListener("transitionend", () => {
                        this.startInteraction()
                        this.checkWinLose(guess, array)
                    }, { once: true })
                }
            }, { once: true })
        },
        showAlert(message, duration = 1000) {
            const alert = document.createElement("div") // get the empty alert div
            alert.textContent = message // add message
            alert.classList.add("alert") // add alert class
            this.alertContainer.prepend(alert)
            if (duration == null) return
            setTimeout(() => {
                alert.classList.add("hide")
                alert.addEventListener("transitionend", () => {
                    alert.remove()
                })
            }, duration)
        },
        shakeTiles(tiles) {
            tiles.forEach(tile => {
                tile.classList.add("shake")
                tile.addEventListener("animationend", () => {
                    tile.classList.remove("shake")
                }, { once: true })
            })
        },
        checkWinLose(guess, tiles) {
            if (guess === this.targetWord) {
                this.showAlert("Wow! You've won! I didn't think you could do it!", 5000)
                this.danceTiles(tiles)
                this.stopInteraction()
                return
            }

            const remainingTiles = this.guessGrid.querySelectorAll(":not([data-letter])") // get all empty tiles

            if (remainingTiles.length === 0) { // if no more remaining tiles
                this.showAlert("🚨LOSER DETECTED!🚨")
                this.showAlert(`The word was: ${this.targetWord.toUpperCase()}`, null)
                this.stopInteraction()
            }
        },
        danceTiles(tiles) {
            tiles.forEach((tile, index) => {
                setTimeout(() => {
                    tile.classList.add("dance")
                    tile.addEventListener(
                        "animationend",
                        () => {
                            tile.classList.remove("dance")
                        },
                        { once: true }
                    )
                }, (index * DANCE_ANIMATION_DURATION) / 5)
            })
        },
    },
};
</script>
