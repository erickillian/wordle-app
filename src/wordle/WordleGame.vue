<template>
    <div>
        <!--v-overlay 
            :value="winOverlay" 
            :z-index=1
        >
            You won!
            <v-btn
                color="success"
                v-on:click="closeWinOverlay"
            >
                Close
            </v-btn>
        </v-overlay-->
        <h1 class="header">Wordle</h1>
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
import JSConfetti from 'js-confetti'

// CONSTANTS
const WORD_LENGTH = 5;
const FLIP_ANIMATION_DELAY = 300
const FLIP_ANIMATION_LENGTH = 300

const BOUNCE_ANIMATION_DELAY = 30
const BOUNCE_ANIMATION_LENGTH = 400

const TWIRL_ANIMATION_DELAY = 0
const TWIRL_ANIMATION_LENGTH = 1500

const DANCE_ANIMATION_DELAY = 50
const ANIMATION_LENGTH = 500

export default {
    name: "WordleGame",
    // components: { SimpleCard, LeadersCard, BigNumberCard },
    mounted() {
        this.guessGrid = this.$el.querySelector("[data-guess-grid]");
        this.keyboard = this.$el.querySelector("[data-keyboard]");
        this.alertContainer = this.$el.querySelector("[data-alert-container]"); // get the empty div container for alerts
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
            this.checkInteraction()
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
            winOverlay: false,
            guessed: false,
        };
    },
    methods: {
        ...mapActions('wordle', [
            'guess',
            'status',
        ]),
        ...mapState({
            wordle: state=> state.wordle
        }),
        startInteraction() { // start listening for clicks and keypresses
            console.log("Starting Interaction");
            document.addEventListener("click", this.handleMouseClick);
            document.addEventListener("keydown", this.handleKeyPress);
        },
        stopInteraction() { // remove the event listeners for clicks and keypresses, effectively making the user unable to interact or type anything
            console.log("Stopping Interaction");
            document.removeEventListener("click", this.handleMouseClick);
            document.removeEventListener("keydown", this.handleKeyPress);
        },
        closeWinOverlay() {
            this.winOverlay = false;
        },
        handleMouseClick(e) {
            if (e.target.matches("[data-key")) { // if event target is a key, press that key
                this.pressKey(e.target.dataset.key);
            }
            else if (e.target.matches("[data-enter]")) { // if user clicks enter, submit the guess
                this.submitGuess();
            }
            else if (e.target.matches("[data-delete]") || e.target.parentElement.matches("[data-delete]") || e.target.parentElement.parentElement.matches("[data-delete]")) { // if user clicks delete, remove that key
                this.deleteKey();
            }
        },
        handleKeyPress(e) {
            if (e.key === "Enter") { // if the key is enter, submit guess
                this.submitGuess()
                return
            }
            else if (e.key === "Backspace" || e.key === "Delete") { // if user presses backspace or delete, delete key
                this.deleteKey()
            }
            else if (e.key.match(/^[a-z]$/)) { // regex for one single letter between a and z
                this.pressKey(e.key)
            }
        },
        pressKey(key) { // add key to first tile in grid
            const activeTiles = this.getActiveTiles() // get array of active tiles
            if (activeTiles.length >= WORD_LENGTH) return // make sure that user cannot keep typing after 5 letters
            
            const nextTile = this.guessGrid.querySelector(":not([data-letter])") // returns the first tile that doesn't have a value
            nextTile.dataset.letter = key.toLowerCase() // add the letter to the tile's dataset
            nextTile.textContent = key // make the html the key
            nextTile.dataset.state = "active" // set it to active
            nextTile.classList.add("pop")
            nextTile.addEventListener(
                "animationend",
                () => {
                    nextTile.classList.remove("pop")
                },
                { once: true }
            )
            
            this.inputs.guess += key.toLowerCase()
        },
        deleteKey() {
            const activeTiles = this.getActiveTiles(); // get array of active tiles
            const lastTile = activeTiles[activeTiles.length - 1]; // get the last active tile
            if (!lastTile) return; // if that tile doesn't have any content, return
            lastTile.textContent = ""; // set the text content to an empty string
            delete lastTile.dataset.state; // delete active state
            delete lastTile.dataset.letter; // delete letter dataset
            this.inputs.guess = this.inputs.guess.slice(0, -1);
        },
        getActiveTiles() {
            // return all the tiles that have the state of active
            return this.guessGrid.querySelectorAll('[data-state="active"]');
        },
        getFilledTiles() {
            // return all the tiles that are filled with a letter
            return this.guessGrid.querySelectorAll('[data-letter]');
        },
        submitGuess() {
            this.stopInteraction()
            const activeTiles = [...this.getActiveTiles()] // get the array of active tiles
            if (activeTiles.length !== WORD_LENGTH) { // if the guess isn't long enough, can't submit it!
                this.showAlert("Not enough letters!")
                this.shakeTiles(activeTiles)
                this.startInteraction()
                return
            }
            const guess = activeTiles.reduce((word, tile) => { // sum the array of individual letters into a string
                return word + tile.dataset.letter
            }, "") // returns a string

            if (this.guessed == false) {
                this.guess({ guess: guess });
                this.guessed = true;
            }
            
            // activeTiles.forEach((...params) => this.flipTile(...params, guess)) // flip tile animation
        },
        initialGuesses() {
            if (this.$store.state.wordle.status_loading == false) {
                const guess_history = this.$store.state.wordle.info.guess_history;
                const correct = this.$store.state.wordle.info.correct;
                
                for (var i=0; i < guess_history.length; i++) {
                    const nextTile = this.guessGrid.querySelector(":not([data-letter])");
                    const letter = guess_history[i].toLowerCase()
                    nextTile.textContent = letter
                    nextTile.dataset.letter = letter
                    const key = this.keyboard.querySelector(`[data-key="${letter}"i]`) 
                    if (key) {
                        if (correct[i] == "0") {
                            nextTile.dataset.state = "wrong"
                            key.classList.add("wrong")
                        }
                        if (correct[i] == "1") {
                            nextTile.dataset.state = "wrong-location"
                            key.classList.add("wrong-location")
                        }
                        if (correct[i] == "2") {
                            nextTile.dataset.state = "correct"
                            key.classList.add("correct")
                        }
                    }
                }
                var time = this.bounceTiles();
                setTimeout(() => {
                    this.checkWinLose()
                }, time);
            }
        },
        checkInteraction() {
            if (this.$store.state.wordle.info.solved == false) {
                this.startInteraction();
            }
        },

        checkWinLose() {
            this.guessed = false;
            if (this.$store.state.wordle.info.solved == true) {
                console.log("solved")
                this.twirlWinningTiles();
                this.word = this.$store.state.wordle.info.guess_history.slice(-WORD_LENGTH);
                this.winOverlay = true;
                const jsConfetti = new JSConfetti()
                jsConfetti.addConfetti({
                    confettiNumber: 500,
                    confettiColors: [
                        '#3876bc', '#ffffff',
                    ],
                })
            } else {
                this.startInteraction()
            }
        },
        guessOk() {
            const guess = this.$store.state.wordle.info.guess_history.slice(-WORD_LENGTH);
            const correct = this.$store.state.wordle.info.correct.slice(-WORD_LENGTH);
            const activeTiles = this.getActiveTiles()


            for (let i = 0; i < activeTiles.length; i++) {
                let tile = activeTiles[i];
                const letter = tile.dataset.letter           
                const key = this.keyboard.querySelector(`[data-key="${letter}"i]`) // get each key - the i makes it case insensitivehel

                setTimeout(() => {
                    tile.classList.add("flip")
                }, i * FLIP_ANIMATION_DELAY)

                tile.addEventListener("transitionend", () => {
                    tile.classList.remove("flip") // remvoe flip class for animation
                    if (correct[i] === "2") {
                        tile.dataset.state = "correct"
                        key.classList.add("correct") // while flipping, if it's the right location and right letter, add correct class
                    } else if (correct[i] === "1") { // otherwise if word includes letter, add wrong location class
                        tile.dataset.state = "wrong-location"
                        key.classList.add("wrong-location")
                    } else if (correct[i] === "0") { // else add wrong class
                        tile.dataset.state = "wrong"
                        key.classList.add("wrong")
                    }
                })
            }            
            setTimeout(() => {
                this.checkWinLose()
            }, ((WORD_LENGTH) * FLIP_ANIMATION_DELAY)+FLIP_ANIMATION_LENGTH);
        },
        guessError() {
            const activeTiles = [...this.getActiveTiles()]
            this.shakeTiles(activeTiles)// flip tile animation
            this.showAlert("Guess Error")
            this.checkWinLose()
        },
        showAlert(message, DELAY = 1000) {
            const alert = document.createElement("div") // get the empty alert div
            alert.textContent = message // add message
            alert.classList.add("alert") // add alert class
            this.alertContainer.prepend(alert)
            if (DELAY == null) return
            setTimeout(() => {
                alert.classList.add("hide")
                alert.addEventListener("transitionend", () => {
                    alert.remove()
                })
            }, DELAY)
        },
        shakeTiles(tiles) {
            tiles.forEach(tile => {
                tile.classList.add("shake")
                tile.addEventListener("animationend", () => {
                    tile.classList.remove("shake")
                }, { once: true })
            })
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
                }, (index * DANCE_ANIMATION_DELAY))
            })
        },
        bounceTiles() {
            const allTiles = this.getFilledTiles();
            for (let i = 0; i < allTiles.length; i++) {
                const tile = allTiles[i]
                setTimeout(() => {
                    tile.classList.add("bounce")
                    tile.addEventListener(
                        "animationend",
                        () => {
                            tile.classList.remove("bounce")
                        },
                        { once: true }
                    )
                }, (i * BOUNCE_ANIMATION_DELAY))
                
            }
            return (allTiles.length*BOUNCE_ANIMATION_DELAY+BOUNCE_ANIMATION_LENGTH)
        },
        twirlWinningTiles() {
            var time = 0;
            const allTiles = this.getFilledTiles();
            for (let i = allTiles.length-WORD_LENGTH; i < allTiles.length; i++) {
                const tile = allTiles[i]
                setTimeout(() => {
                    tile.classList.add("twirl")
                    tile.classList.add("rainbow");
                    tile.addEventListener(
                        "animationend",
                        () => {
                            tile.classList.remove("twirl")
                        },
                        { once: true }
                    )
                }, (i * TWIRL_ANIMATION_DELAY))
                time += TWIRL_ANIMATION_DELAY;
            }
            return (WORD_LENGTH*BOUNCE_ANIMATION_DELAY+BOUNCE_ANIMATION_LENGTH)
        }
    },
};
</script>
