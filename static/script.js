document.getElementById('start-reading').addEventListener('click', function() {
    var text = document.getElementById('texte-container').getAttribute('data-texte');
    var words = text.split(' '); // Divisez le texte en mots
    var index = 0;
    var msg = new SpeechSynthesisUtterance();

    // Ajustez la vitesse de lecture en modifiant la propriété 'rate'
    msg.rate = 3; // Augmentez la vitesse de 50%

    function speakNextPhrase() {
        if (index < words.length) {
            // Regroupez les mots en une phrase
            var phrase = words.slice(index, index + 5).join(' '); // Lire jusqu'à 5 mots à la fois
            msg.text = phrase;
            msg.onend = function() {
                document.getElementById('pdf-content').innerHTML += phrase + ' ';
                index += phrase.split(' ').length; // Avancer l'index en fonction du nombre de mots lus
                speakNextPhrase();
            };
            window.speechSynthesis.speak(msg);
        }
    }

    speakNextPhrase();
});
