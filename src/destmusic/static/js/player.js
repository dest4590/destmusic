const musicPlayer = new Audio()

musicPlayer.onended = (event) => {
    temp_elem = musicPlayer.elem // temp
    temp_song = temp_elem.parentElement.parentElement // temp

    playStop(musicPlayer.elem)

    songs = temp_elem.parentElement.parentElement.parentElement.children

    for (const e of songs) {
        if (e != temp_song) {
            play(e.querySelector('div[id="song-buttons"] a[onclick="play(this)"]'), false)
            break
        }
    }
}

const filterDelay = 2000
const maxBrightness = '0.4'
const intervals = []

function playStart(elem, fade = true) {
    // Play
    
    setTimeout(() => { document.body.style.backdropFilter = `brightness(${maxBrightness})` }, filterDelay + 20)

    document.musicControl.style.opacity = 1
    document.musicControl.style.marginTop = '15px'
    document.musicControl.style.pointerEvents = 'all'

    try {
        const colorThief = new ColorThief()

        const colors = colorThief.getPalette(elem.parentElement.parentElement.querySelector('img[id="song-artwork"]'), 3)

        const darkenedPalette = []

        for (const color of colors) {
            const darkenedColor = color.map(value => Math.round(value * 0.5))
            darkenedPalette.push(darkenedColor)
        }

        bg = setTimeout(() => {
            document.body.style.backgroundImage = `linear-gradient(${Math.floor(Math.random() * 360)}deg, ` + darkenedPalette.map(color => `rgb(${color[0]}, ${color[1]}, ${color[2]})`).join(', ') + ')'
        }, filterDelay + 10)

        document.bgTimeout = bg
    }

    catch (e) {
        document.body.style.backgroundColor = 'black'
    }

    document.querySelectorAll('div[id="song-buttons"] img[id="play-img"]').forEach((element) => {
        element.src = '/static/img/svg/play.svg'
    })

    musicPlayer.play()

    if (fade) {
        // volumefadeIn(musicPlayer)
    }

    elem.children[0].src = '/static/img/svg/stop.svg'
}

function playStop(elem) {
    // Pause
    document.body.style.backdropFilter = 'brightness(0)'

    setTimeout(() => {
        document.body.style.backgroundImage = 'linear-gradient(#000, #000)'
    }, filterDelay)

    document.musicControl.style.opacity = 0
    document.musicControl.style.marginTop = '0px'
    document.musicControl.style.pointerEvents = 'none'

    musicPlayer.paused = true
    musicPlayer.src = ""
    musicPlayer.elem = null // reset element on musicPlayer
    elem.children[0].src = '/static/img/svg/play.svg' // play icon
}

function changeSong(songUrl) {
    musicPlayer.src = songUrl

    document.body.style.backdropFilter = 'brightness(0)'

    setTimeout(() => {
        document.body.style.backgroundImage = 'linear-gradient(#000, #000)'
    }, filterDelay)
}

function play(elem, fade = true) {
    const songUrl = elem.parentElement.querySelector('a[download]').href

    musicPlayer.elem = elem

    clearInterval(document.bgTimeout)

    const img = elem.children[0]

    if (img.src.includes('play.svg')) {
        changeSong(songUrl)
        playStart(elem, fade)
    } else {
        playStop(elem)
    }
}

function changeVolume(e) {
    musicPlayer.volume = e.value / 100
    set('volume', e.value / 100)
}