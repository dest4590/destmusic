function get(s) {
    return localStorage.getItem(s)
}

function set(s, v) {
    return localStorage.setItem(s, v)
}

function animateSongCards() {
    var index = 0

    for (const element of document.querySelectorAll('div.song')) {
        const timeout = 30 * (index++)

        setTimeout(() => {
            element.style.marginTop = '20px'
            element.style.opacity = 1
        }, timeout)

        setTimeout(() => element.querySelector('p[id="song-name"]').style.opacity = 1, timeout + 400)
        setTimeout(() => element.querySelector('p[id="song-author"]').style.opacity = 1, timeout + 600)
    }
}

function isElementVisible(element) {
    var rect = element.getBoundingClientRect();
    var windowHeight = window.innerHeight || document.documentElement.clientHeight;
    var windowWidth = window.innerWidth || document.documentElement.clientWidth;

    var verticallyVisible = (rect.top <= windowHeight && rect.bottom >= 0);
    var horizontallyVisible = (rect.left <= windowWidth && rect.right >= 0);

    return verticallyVisible && horizontallyVisible;
}

function scrollToElement(element) {
    var elementRect = element.getBoundingClientRect();
    var offset = elementRect.top + elementRect.height / 2 - window.innerHeight / 2;

    window.scrollTo({
        top: offset,
        behavior: 'smooth'
    });
}

function search(e, query = null) {
    if (e === null) {
        var searchTerm = query[0]
        var searchElem = query[1]

        for (const e of searchElem.parentElement.children) {
            if (e !== searchElem) {
                e.style.transform = 'none'
                e.style.marginLeft = ''
                e.style.marginRight = ''
                e.style.opacity = 0.4
            }

            else {
                e.style.marginLeft = '5px'
                e.style.marginRight = '5px'
                e.style.transform = 'scale(1.1)'
                e.style.opacity = 1
            }
        }

    }
    else {
        Array.from(document.querySelectorAll('div.genres p')).forEach(e => {
            e.removeAttribute("style");
        })

        var searchTerm = e.toLowerCase()
    }

    const songs = document.querySelectorAll('div.song')

    if (searchTerm !== "") {
        var count = 0
        songs.forEach((song) => {
            const found = [1, 2, 3].some(index => song.children[index].textContent.toLowerCase().startsWith(searchTerm))
            if (found) {
                elem = document.getElementById(song.id)

                if (count == 0 & !isElementVisible(elem)) {
                    scrollToElement(elem)
                }

                song.style.transform = 'scale(1.05)'
                song.style.opacity = 1
                song.style.filter = 'none'
                count += 1
            } else {
                song.style.transform = 'none'
                song.style.opacity = 0.4
                song.style.filter = 'blur(2px)'
            }
        })

        document.title = `DestMusic (${count})`

    } else {
        document.title = 'DestMusic'

        // reset styles
        songs.forEach((song) => {
            song.style.transform = 'none'
            song.style.opacity = 1
            song.style.filter = 'none'
        })
    }
}

window.onload = () => {
    const isHomepage = ['/', '/develop'].includes(location.pathname)
    const isAuthorPage = location.pathname.includes('author')

    if (isHomepage) {
        animateSongCards()

        if (get('volume') == null) {
            set('volume', 0.1)
        }

        musicPlayer.volume = parseFloat(get('volume'))
        document.querySelector('#song-volume').value = parseFloat(get('volume')) * 100

        document.musicControl = document.querySelector('div.control') // player.js

        document.querySelector('div[class="info"]').style.opacity = 1
        document.querySelector('div[class="genres"]').style.opacity = 1
        document.getElementById('song-search').oninput = (e) => { search(e.target.value) }
    }

    if (isAuthorPage) {
        const hr = document.querySelector('div[class="author-info"] hr')

        hr.style.opacity = 1
        setTimeout(() => {
            hr.style.marginLeft = '5%'
            hr.style.marginRight = '5%'
        }, 100)

        setTimeout(animateSongCards, 150)
    }
}

function copyUpdate(e) {
    var version = e.parentElement.getAttribute('version')
    navigator.clipboard.writeText('https://music.dest4590.lol/updates/' + version)
}