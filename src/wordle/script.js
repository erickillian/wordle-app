// CONSTANTS
const WORD_LENGTH = 5;
const FLIP_ANIMATION_DURATION = 750
const DANCE_ANIMATION_DURATION = 500

const keyboard = document.querySelector("[data-keyboard]") // get the keyboard
const alertContainer = document.querySelector("[data-alert-container]") // get the empty div container for alerts
const guessGrid = document.querySelector("[data-guess-grid]") // get the grid of tiles
const offsetFromDate = new Date(2022, 0, 1); // starting date
const msOffset = Date.now() - offsetFromDate // get difference in milliseconds
const dayOffset = msOffset / 1000 / 60 / 60 / 24 // convert to days
const targetWord = targetWords[Math.floor(dayOffset)] // get the word in the array at that index, and every day, a new index

startInteraction()

function startInteraction() { // start listening for clicks and keypresses
    document.addEventListener("click", handleMouseClick)
    document.addEventListener("keydown", handleKeyPress)
}

function stopInteraction() { // remove the event listeners for clicks and keypresses, effectively making the user unable to interact or type anything
    document.removeEventListener("click", handleMouseClick)
    document.removeEventListener("keydown", handleKeyPress)
}

function handleMouseClick(e) {
    if (e.target.matches("[data-key")) { // if event target is a key, press that key
        pressKey(e.target.dataset.key)
        return
    }

    if (e.target.matches("[data-enter]")) { // if user clicks enter, submit the guess
        submitGuess()
        return
    }

    if (e.target.matches("[data-delete]")) { // if user clicks delete, remove that key
        deleteKey()
        return
    }
}

function handleKeyPress(e) {
    if (e.key === "Enter") { // if the key is enter, submit guess
        submitGuess()
        return
    }

    if (e.key === "Backspace" || e.key === "Delete") { // if user presses backspace or delete, delete key
        deleteKey()
    }

    if (e.key.match(/^[a-z]$/)) { // regex for one single letter between a and z
        pressKey(e.key)
        return
    }
}

function pressKey(key) { // add key to first tile in grid
    const activeTiles = getActiveTiles() // get array of active tiles
    if (activeTiles.length >= WORD_LENGTH) return // make sure that user cannot keep typing after 5 letters
    const nextTile = guessGrid.querySelector(":not([data-letter])") // returns the first tile that doesn't have a value
    nextTile.dataset.letter = key.toLowerCase() // add the letter to the tile's dataset
    nextTile.textContent = key // make the html the key
    nextTile.dataset.state = "active" // set it to active
}

function deleteKey() {
    const activeTiles = getActiveTiles() // get array of active tiles
    const lastTile = activeTiles[activeTiles.length - 1] // get the last active tile
    if (lastTile === null) return // if that tile doesn't have any content, return
    lastTile.textContent = "" // set the text content to an empty string
    delete lastTile.dataset.state // delete active state
    delete lastTile.dataset.letter // delete letter dataset
}

function getActiveTiles() {
    return guessGrid.querySelectorAll('[data-state="active"]')
    // return all the tiles that have the state of active
}

function submitGuess() {
    const activeTiles = [...getActiveTiles()] // get the array of active tiles
    if (activeTiles.length !== WORD_LENGTH) { // if the guess isn't long enough, can't submit it!
        showAlert("Not enough letters!")
        shakeTiles(activeTiles)
        return
    }

    const guess = activeTiles.reduce((word, tile) => { // sum the array of individual letters into a string
        return word + tile.dataset.letter
    }, "") // returns a string

    if (!dictionary.includes(guess)) { // when the guess isn't a real word
        showAlert("Not in word list!")
        shakeTiles(activeTiles)
        return
    }

    stopInteraction()
    activeTiles.forEach((...params) => flipTile(...params, guess)) // flip tile animation
}

function flipTile(tile, index, array, guess) {
    const letter = tile.dataset.letter
    const key = keyboard.querySelector(`[data-key="${letter}"i]`) // get each key - the i makes it case insensitive
    setTimeout(() => {
        tile.classList.add("flip")
    }, index * FLIP_ANIMATION_DURATION / 2)

    tile.addEventListener("transitionend", () => {
        tile.classList.remove("flip") // remvoe flip class for animation
        if (targetWord[index] === letter) {
            tile.dataset.state = "correct"
            key.classList.add("correct") // while flipping, if it's the right location and right letter, add correct class
        } else if (targetWord.includes(letter)) { // otherwise if word includes letter, add wrong location class
            tile.dataset.state = "wrong-location"
            key.classList.add("wrong-location")
        } else { // else add wrong class
            tile.dataset.state = "wrong"
            key.classList.add("wrong")
        }

        if (index === array.length - 1) { // if last tile, user can start interacting again
            tile.addEventListener("transitionend", () => {
                startInteraction()
                checkWinLose(guess, array)
            }, { once: true })
        }
    }, { once: true })
}

function showAlert(message, duration = 1000) {
    const alert = document.createElement("div") // get the empty alert div
    alert.textContent = message // add message
    alert.classList.add("alert") // add alert class
    alertContainer.prepend(alert)
    if (duration == null) return
    setTimeout(() => {
        alert.classList.add("hide")
        alert.addEventListener("transitionend", () => {
            alert.remove()
        })
    }, duration)
}

function shakeTiles(tiles) {
    tiles.forEach(tile => {
        tile.classList.add("shake")
        tile.addEventListener("animationend", () => {
            tile.classList.remove("shake")
        }, { once: true })
    })
}

function checkWinLose(guess, tiles) {
    if (guess === targetWord) {
        showAlert("Wow! You've won! I didn't think you could do it!", 5000)
        danceTiles(tiles)
        stopInteraction()
        return
    }

    const remainingTiles = guessGrid.querySelectorAll(":not([data-letter])") // get all empty tiles

    if (remainingTiles.length === 0) { // if no more remaining tiles
        showAlert("🚨LOSER DETECTED!🚨")
        showAlert(`The word was: ${targetWord.toUpperCase()}`, null)
        stopInteraction
    }
}

function danceTiles(tiles) {
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
}